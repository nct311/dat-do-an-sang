#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
May chu dat do an sang - Xoi - Banh mi - Drink
Chi dung thu vien chuan cua Python (khong can cai them gi).
Chay:  python server.py        (Windows: py server.py)
Mo Chrome: http://localhost:8000
Khach cung WiFi: http://<IP-cua-may-ban>:8000
Don hang luu vao don-hang.txt + orders.json ngay trong thu muc nay.
"""
import hashlib
import json
import math
import os
import random
import secrets
import time
from urllib.parse import quote
from xml.sax.saxutils import escape as xml_escape
from collections import deque
from datetime import datetime, timedelta, timezone
# Gio Viet Nam (UTC+7) — may chu Render chay gio UTC nen phai cong 7 gio
VN_TZ = timezone(timedelta(hours=7))
def now_vn():
    return datetime.now(VN_TZ)
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")
ORDERS_FILE = os.path.join(BASE_DIR, "orders.json")
ORDERS_TXT = os.path.join(BASE_DIR, "don-hang.txt")
PORT = int(os.environ.get("PORT", "8000"))  # Render cap cong qua bien moi truong PORT
OWNER_PHONE = "0358961119"  # so dien thoai cua quan

MENU = [
    {"id": 1, "cat": "xoi", "name": "Xôi trứng (2 trứng)", "price": 28000},
    {"id": 2, "cat": "xoi", "name": "Xôi pate trứng", "price": 23000},
    {"id": 3, "cat": "xoi", "name": "Xôi xúc xích", "price": 23000},
    {"id": 4, "cat": "xoi", "name": "Xôi chả", "price": 23000},
    {"id": 5, "cat": "xoi", "name": "Xôi khô bò", "price": 23000},
    {"id": 6, "cat": "xoi", "name": "Xôi lạp xưởng", "price": 23000},
    {"id": 7, "cat": "xoi", "name": "Xôi pate chả", "price": 28000},
    {"id": 8, "cat": "xoi", "name": "Xôi trứng xúc xích", "price": 28000},
    {"id": 9, "cat": "xoi", "name": "Xôi trứng chả", "price": 28000},
    {"id": 10, "cat": "xoi", "name": "Xôi trứng bò khô", "price": 28000},
    {"id": 11, "cat": "xoi", "name": "Xôi thập cẩm", "price": 43000},
    {"id": 12, "cat": "banhmi", "name": "Bánh mì trứng", "price": 16000},
    {"id": 13, "cat": "banhmi", "name": "Bánh mì pate trứng", "price": 20000},
    {"id": 14, "cat": "banhmi", "name": "Bánh mì xúc xích", "price": 18000},
    {"id": 15, "cat": "banhmi", "name": "Bánh mì chả", "price": 18000},
    {"id": 16, "cat": "banhmi", "name": "Bánh mì khô bò", "price": 18000},
    {"id": 17, "cat": "banhmi", "name": "Bánh mì lạp xưởng", "price": 18000},
    {"id": 18, "cat": "banhmi", "name": "Bánh mì pate chả", "price": 23000},
    {"id": 19, "cat": "banhmi", "name": "Bánh mì trứng xúc xích", "price": 23000},
    {"id": 20, "cat": "banhmi", "name": "Bánh mì trứng chả", "price": 23000},
    {"id": 21, "cat": "banhmi", "name": "Bánh mì trứng khô bò", "price": 23000},
    {"id": 22, "cat": "banhmi", "name": "Bánh mì thập cẩm", "price": 23000},
    {"id": 23, "cat": "banhmi", "name": "Bánh bao xá xíu thập cẩm 2 trứng", "price": 18000},
    {"id": 24, "cat": "drink", "name": "Trà chanh / tắc", "price": 15000},
    {"id": 25, "cat": "drink", "name": "Trà chanh / tắc trân châu", "price": 23000},
    {"id": 26, "cat": "drink", "name": "Trà chanh leo", "price": 18000},
    {"id": 27, "cat": "drink", "name": "Trà chanh leo trân châu", "price": 23000},
    {"id": 28, "cat": "drink", "name": "Trà đá / nhân trần / vối", "price": 8000},
]
MENU_BY_ID = {m["id"]: m for m in MENU}
STATUS_LABEL = {"moi": "Mới", "xac-nhan": "Đã xác nhận", "hoan-thanh": "Hoàn thành", "huy": "Đã hủy"}

LOCK = Lock()
TOKENS = {}  # token -> phone (chi luu trong bo nho, khoi dong lai may chu thi dang nhap lai)

# --- Bao mat & chong spam ---
MAX_BODY_SIZE = 65536  # 64KB: moi request POST vuot qua deu bi tu choi (413)
MAX_NAME_LEN = 50
MAX_NOTE_LEN = 200
MAX_METHOD_LEN = 30
MAX_TIME_LEN = 50
MAX_ADDRESS_LEN = 100
MAX_QTY_PER_DISH = 10   # moi mon toi da 10 phan / don
MAX_ITEMS_PER_ORDER = 20  # moi don toi da 20 mon (tong so luong)
MIN_FORM_TIME_MS = 800  # don gui < 0.8 giay sau khi mo trang -> coi la bot
ORDER_COOLDOWN_S = 3    # cung 1 IP / cung 1 ten: don thanh cong cach nhau it nhat 3 giay
# Gioi han so request ghi / IP / phut: (so lan toi da, cua so giay)
RATE_LIMITS = {"order": (10, 60), "login": (10, 60), "register": (5, 60), "other": (30, 60),
               # Tai trang / goi thuc don: 30 lan / IP / phut (nguoi thuong chi tai
               # 1-2 lan). KHONG gioi han /api/orders (polling 5 giay/lan la binh thuong).
               "page": (30, 60), "menu": (30, 60),
               # Lay ma captcha: 30 lan / IP / phut (du cho nguoi that bam
               # "Doi cau khac" vai lan; bot lay ma lien tuc se bi chan).
               "captcha": (30, 60)}
_rate_buckets = {}   # (ip, key) -> deque[thoi diem monotonic]
_rate_lock = Lock()
_last_order_ip = {}    # ip -> thoi diem don thanh cong gan nhat
_last_order_name = {}  # ten khach (viet thuong) -> thoi diem don thanh cong gan nhat

# --- Ma phien dat hang (order token) ---
# GET /api/menu cap 1 ma ngan han, gan voi IP, han 10 phut. Don POST bat
# buoc phai kem ma nay: bot POST thang ma khong mo trang lay thuc don se bi
# chan. Ma chi dung duoc cho 1 don thanh cong (xoa ngay khi don duoc tao).
ORDER_TOKEN_TTL_S = 600  # 10 phut
_order_tokens = {}  # token -> (ip, het han monotonic)
_order_token_lock = Lock()

# --- Khoa dang nhap khi doan mat khau sai nhieu lan ---
# 5 lan sai cho cung 1 SDT trong 10 phut -> khoa SDT do 15 phut.
LOGIN_MAX_FAILS = 5
LOGIN_FAIL_WINDOW_S = 600   # 10 phut
LOGIN_LOCK_S = 900          # 15 phut
_login_failures = {}  # phone -> deque[thoi diem monotonic]
_login_locks = {}     # phone -> het khoa monotonic
_login_lock = Lock()


def issue_order_token(ip):
    """Cap ma phien dat hang moi cho IP nay; dong thoi don dep ma het han."""
    now = time.monotonic()
    with _order_token_lock:
        expired = [t for t, (_, exp) in _order_tokens.items() if exp <= now]
        for t in expired:
            del _order_tokens[t]
        token = secrets.token_hex(16)
        _order_tokens[token] = (ip, now + ORDER_TOKEN_TTL_S)
        return token


def valid_order_token(token, ip):
    """True neu ma ton tai, dung IP da cap va con han (chua xoa ma o day;
    ma se bi xoa khi don thanh cong de chi dung duoc 1 lan)."""
    if not token or not isinstance(token, str):
        return False
    now = time.monotonic()
    with _order_token_lock:
        rec = _order_tokens.get(token)
        if not rec:
            return False
        tip, exp = rec
        return tip == ip and exp > now


def login_locked(phone):
    """(True, so giay con lai) neu SDT dang bi khoa; het khoa thi tu mo."""
    now = time.monotonic()
    with _login_lock:
        until = _login_locks.get(phone)
        if until is not None:
            if now < until:
                return True, int(until - now)
            del _login_locks[phone]
        return False, 0


def record_login_failure(phone):
    """Ghi 1 lan dang nhap sai; du 5 lan trong 10 phut thi khoa 15 phut."""
    now = time.monotonic()
    with _login_lock:
        dq = _login_failures.setdefault(phone, deque())
        while dq and dq[0] <= now - LOGIN_FAIL_WINDOW_S:
            dq.popleft()
        dq.append(now)
        if len(dq) >= LOGIN_MAX_FAILS:
            _login_locks[phone] = now + LOGIN_LOCK_S
            _login_failures.pop(phone, None)


def clear_login_failures(phone):
    """Dang nhap dung: xoa het lich su sai + mo khoa (neu co) cua SDT nay."""
    with _login_lock:
        _login_failures.pop(phone, None)
        _login_locks.pop(phone, None)


# --- Captcha keo (drag slider puzzle, tu xay, khong dich vu ngoai) ---
# Thu thach: nen 300x150 co 1 cho trong hinh manh ghep o vi tri x ngau
# nhien; nguoi dung keo manh ghep (cung hinh, cung hoa van) vao dung cho
# trong do. Sai so cho phep ±6px. Moi captcha_id chi cho sai toi da 5 lan,
# han dung 3 phut. Qua duoc thi nhan bypass token 10 phut (gan voi IP):
# trong 10 phut do IP duoc mien khoi cac gioi han spam (rate limit dat
# don, cooldown 3 giay, gioi han tai trang/thuc don) — nhung van phai co
# order_token, honeypot, min-time va gioi han so luong nhu binh thuong.
# Vi tri dung (x cua cho trong) CHI luu o may chu, khong bao gio tra ve
# cho trinh duyet.
CAPTCHA_TTL_S = 180        # 3 phut
CAPTCHA_MAX_FAILS = 5
CAPTCHA_BYPASS_TTL_S = 600  # 10 phut
CAPTCHA_BG_W, CAPTCHA_BG_H = 300, 150   # kich thuoc nen puzzle (px)
CAPTCHA_PIECE_W, CAPTCHA_PIECE_H = 55, 46  # manh ghep (gom ca tab loi ra)
CAPTCHA_GAP_Y = 52          # vi tri doc cua cho trong / manh ghep (px)
CAPTCHA_GAP_MIN_X, CAPTCHA_GAP_MAX_X = 40, 220  # cho trong nam trong khoang nay
CAPTCHA_TOLERANCE_PX = 6    # sai so cho phep khi keo (px)
_captchas = {}       # captcha_id -> {"x", "ip", "exp", "fails"}
_captcha_bypass = {}  # bypass_token -> (ip, het han monotonic)
_captcha_lock = Lock()


def _piece_path(x, y):
    """Duong vien hinh manh ghep (vuong bo tron 46x46 + 1 tab loi ra ben
    phai) dat o goc trai-tren (x, y). Dung chung cho ca cho trong tren nen
    va hinh manh ghep de hai hinh khop nhau hoan toan."""
    return (
        f"M {x + 6} {y} H {x + 40} A 6 6 0 0 1 {x + 46} {y + 6} V {y + 14} "
        f"A 9 9 0 0 1 {x + 46} {y + 32} V {y + 40} A 6 6 0 0 1 {x + 40} {y + 46} "
        f"H {x + 6} A 6 6 0 0 1 {x} {y + 40} V {y + 6} A 6 6 0 0 1 {x + 6} {y} Z"
    )


def _captcha_pattern(rng):
    """Hoa van nen ngau nhien: 1 gradient + hinh tron/chu nhat/cham nhieu
    nhieu mau. Tra ve (gradient_svg, [shape, ...]) de nen va manh ghep
    dung chung 1 bo hoa van (manh ghep la dung lat cat cua nen)."""
    g1, g2 = rng.choice([("#FFE8A3", "#F4A261"), ("#B7E4C7", "#2D6A4F"),
                         ("#FFD6A5", "#E76F51"), ("#CAF0F8", "#40916C")])
    grad = (f'<defs><linearGradient id="cg" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="0" x2="{CAPTCHA_BG_W}" y2="{CAPTCHA_BG_H}">'
            f'<stop offset="0" stop-color="{g1}"/>'
            f'<stop offset="1" stop-color="{g2}"/></linearGradient></defs>')
    palette = ["#2D6A4F", "#40916C", "#E9C46A", "#F4A261", "#E76F51",
               "#1B4332", "#F4D58D", "#BC6C25", "#52B788", "#DDA15E"]
    shapes = []
    for _ in range(14):
        shapes.append(f'<circle cx="{rng.randint(0, CAPTCHA_BG_W)}" cy="{rng.randint(0, CAPTCHA_BG_H)}" r="{rng.randint(8, 26)}" fill="{rng.choice(palette)}" opacity="0.85"/>')
    for _ in range(10):
        shapes.append(f'<rect x="{rng.randint(0, 280)}" y="{rng.randint(0, 130)}" width="{rng.randint(10, 30)}" height="{rng.randint(8, 20)}" rx="4" fill="{rng.choice(palette)}" opacity="0.8"/>')
    for _ in range(30):
        shapes.append(f'<circle cx="{rng.randint(0, CAPTCHA_BG_W)}" cy="{rng.randint(0, CAPTCHA_BG_H)}" r="{rng.choice([1, 1.5, 2])}" fill="#FFFDF8" opacity="0.7"/>')
    return grad, shapes


def _captcha_bg_svg(gap_x, grad, shapes):
    """Nen 300x150: gradient + hoa van, voi cho trong hinh manh ghep o
    (gap_x, GAP_Y) to mau + vien trang de nhin ro."""
    gap = _piece_path(gap_x, CAPTCHA_GAP_Y)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{CAPTCHA_BG_W}" height="{CAPTCHA_BG_H}" viewBox="0 0 {CAPTCHA_BG_W} {CAPTCHA_BG_H}">',
             grad,
             f'<rect width="{CAPTCHA_BG_W}" height="{CAPTCHA_BG_H}" fill="url(#cg)"/>',
             *shapes,
             f'<path d="{gap}" fill="rgba(20,16,8,0.55)" stroke="#FFFFFF" stroke-width="2"/>',
             "</svg>"]
    return "".join(parts)


def _captcha_piece_svg(gap_x, grad, shapes):
    """Manh ghep 55x46: lat cat dung vi tri cho trong cua nen (cung hoa
    van, dich chuyen -gap_x/-GAP_Y) roi cat theo duong vien manh ghep."""
    clip = _piece_path(0, 0)
    inner = "".join([f'<rect width="{CAPTCHA_BG_W}" height="{CAPTCHA_BG_H}" fill="url(#cg)"/>',
                     *shapes])
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{CAPTCHA_PIECE_W}" height="{CAPTCHA_PIECE_H}" viewBox="0 0 {CAPTCHA_PIECE_W} {CAPTCHA_PIECE_H}">',
             grad,
             f'<defs><clipPath id="cp"><path d="{clip}"/></clipPath></defs>',
             f'<g clip-path="url(#cp)"><g transform="translate({-gap_x},{-CAPTCHA_GAP_Y})">{inner}</g></g>',
             f'<path d="{clip}" fill="none" stroke="#FFFFFF" stroke-width="2"/>',
             "</svg>"]
    return "".join(parts)


def make_captcha():
    """Tao 1 thu thach moi: (vi tri x cua cho trong, anh nen SVG, anh manh
    ghep SVG). Vi tri dung CHI luu o may chu, khong co trong anh tra ve."""
    rng = random.Random(secrets.token_bytes(16))
    gap_x = rng.randint(CAPTCHA_GAP_MIN_X, CAPTCHA_GAP_MAX_X)
    grad, shapes = _captcha_pattern(rng)
    return gap_x, _captcha_bg_svg(gap_x, grad, shapes), _captcha_piece_svg(gap_x, grad, shapes)


def issue_captcha(ip):
    """Cap ma captcha moi cho IP nay; dong thoi don dep ma het han.
    Tra ve (captcha_id, anh_nen_data_uri, anh_manh_ghep_data_uri)."""
    now = time.monotonic()
    gap_x, bg_svg, piece_svg = make_captcha()
    cid = secrets.token_hex(16)
    with _captcha_lock:
        for k, v in list(_captchas.items()):
            if v["exp"] <= now:
                del _captchas[k]
        _captchas[cid] = {"x": gap_x, "ip": ip,
                          "exp": now + CAPTCHA_TTL_S, "fails": 0}
    print(f"CAPTCHA [{now_vn().strftime('%H:%M:%S')}] IP={ip} — cap ma {cid[:8]}...")
    return (cid,
            "data:image/svg+xml;charset=utf-8," + quote(bg_svg, safe=""),
            "data:image/svg+xml;charset=utf-8," + quote(piece_svg, safe=""))


def _cleanup_captcha_bypass(now):
    for tok, (_, exp) in list(_captcha_bypass.items()):
        if exp <= now:
            del _captcha_bypass[tok]


def verify_captcha(cid, offset, ip):
    """Kiem tra vi tri keo. Tra ve (http_code, code_loi, thong_bao, bypass_token).
    Dung khi |offset - x_cho_trong| <= 6px. Sai qua 5 lan thi huy ma, phai
    lay ma moi."""
    now = time.monotonic()
    with _captcha_lock:
        rec = _captchas.get(cid)
        if not rec or rec["ip"] != ip:
            return (400, "captcha_expired",
                    "Mã xác minh không tồn tại hoặc đã hết hạn, vui lòng bấm Đổi câu khác lấy mã mới.", None)
        if rec["exp"] <= now:
            del _captchas[cid]
            return (400, "captcha_expired",
                    "Mã xác minh đã hết hạn (3 phút), vui lòng bấm Đổi câu khác lấy mã mới.", None)
        if rec["fails"] >= CAPTCHA_MAX_FAILS:
            # Da sai du 5 lan: lan goi tiep theo (du dung hay sai) se huy ma.
            del _captchas[cid]
            print(f"CAPTCHA [{now_vn().strftime('%H:%M:%S')}] IP={ip} — sai qua 5 lan, huy ma {cid[:8]}...")
            return (400, "captcha_locked",
                    "Bạn đã kéo sai quá 5 lần, vui lòng bấm Đổi câu khác lấy mã mới.", None)
        try:
            off = float(offset)
        except Exception:
            off = None
        if off is None or abs(off - rec["x"]) > CAPTCHA_TOLERANCE_PX:
            rec["fails"] += 1
            left = CAPTCHA_MAX_FAILS - rec["fails"]
            print(f"CAPTCHA [{now_vn().strftime('%H:%M:%S')}] IP={ip} — keo sai vi tri (con {left} lan)")
            if left > 0:
                return (400, "captcha_wrong",
                        f"Bạn kéo chưa đúng vị trí, còn {left} lần thử.", None)
            return (400, "captcha_wrong",
                    "Bạn kéo chưa đúng vị trí, mã này đã hết lượt thử.", None)
        del _captchas[cid]
        token = secrets.token_hex(16)
        _captcha_bypass[token] = (ip, now + CAPTCHA_BYPASS_TTL_S)
        print(f"CAPTCHA [{now_vn().strftime('%H:%M:%S')}] IP={ip} — qua xac minh, cap bypass 10 phut")
        return (200, None, "Xác minh thành công.", token)


def valid_captcha_bypass(token, ip):
    """True neu bypass token ton tai, dung IP da cap va con han 10 phut."""
    if not token or not isinstance(token, str):
        return False
    now = time.monotonic()
    with _captcha_lock:
        _cleanup_captcha_bypass(now)
        rec = _captcha_bypass.get(token)
        return bool(rec and rec[0] == ip)


def captcha_bypass_active(ip):
    """True neu IP nay dang co bypass token con han (vd: da qua captcha o
    tab khac). Dung de mien gioi han tai trang/thuc don cho IP do."""
    now = time.monotonic()
    with _captcha_lock:
        _cleanup_captcha_bypass(now)
        return any(tip == ip for tip, _ in _captcha_bypass.values())

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": (
        "default-src 'self'; script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
        "connect-src 'self'; font-src 'self'; object-src 'none'; "
        "base-uri 'self'; frame-ancestors 'none'"
    ),
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Cross-Origin-Resource-Policy": "same-origin",
    "X-Permitted-Cross-Domain-Policies": "none",
}


def clean_text(s, max_len):
    """Loai ky tu dieu khien (giu \n, \t), cat khoang trang 2 dau, gioi han do dai.
    Dung cho ten, ghi chu, hinh thuc, gio nhan, dia chi truoc khi luu/hien."""
    s = str(s or "")
    s = "".join(ch for ch in s if ch in ("\n", "\t") or ord(ch) >= 32)
    return s.strip()[:max_len]


def client_ip(handler):
    """IP that cua client. Render chay sau proxy nen uu tien X-Forwarded-For
    (lay IP dau tien trong chuoi)."""
    xff = handler.headers.get("X-Forwarded-For") or ""
    if xff:
        return xff.split(",")[0].strip() or handler.client_address[0]
    return handler.client_address[0]


def log_block(ip, reason):
    print(f"CHẶN [{now_vn().strftime('%H:%M:%S')}] IP={ip} — {reason}")


def rate_limited(ip, key):
    """True neu IP vuot gioi han cua endpoint `key` trong cua so thoi gian.
    Dem moi lan goi (ke ca request loi) de chan spam/flood."""
    limit, window = RATE_LIMITS.get(key, RATE_LIMITS["other"])
    now = time.monotonic()
    with _rate_lock:
        dq = _rate_buckets.setdefault((ip, key), deque())
        while dq and dq[0] <= now - window:
            dq.popleft()
        if len(dq) >= limit:
            return True
        dq.append(now)
        return False


def order_cooldown_active(ip, name):
    """True neu IP nay hoac ten khach nay vua dat don thanh cong chua du 3 giay."""
    now = time.monotonic()
    with _rate_lock:
        last_ip = _last_order_ip.get(ip)
        if last_ip is not None and now - last_ip < ORDER_COOLDOWN_S:
            return True
        last_name = _last_order_name.get(name.strip().lower())
        if last_name is not None and now - last_name < ORDER_COOLDOWN_S:
            return True
        return False


def mark_order_success(ip, name):
    now = time.monotonic()
    with _rate_lock:
        _last_order_ip[ip] = now
        _last_order_name[name.strip().lower()] = now


def norm_phone(p):
    return "".join(ch for ch in str(p or "") if ch.isdigit())


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def hash_password(password, salt_hex):
    salt = bytes.fromhex(salt_hex)
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000).hex()


def fmt(n):
    return f"{n:,}đ".replace(",", ".")


OWNER_PASSWORD = "quan2026"  # mat khau mac dinh cua tai khoan chu quan


def ensure_owner_account():
    """Tao tai khoan chu quan mac dinh neu chua co (vd: sau khi Render
    deploy lai lam mat users.json). Khong ghi de tai khoan da ton tai."""
    with LOCK:
        users = load_json(USERS_FILE, [])
        if any(norm_phone(u.get("phone")) == OWNER_PHONE for u in users):
            return False
        salt = secrets.token_hex(16)
        users.append({
            "phone": OWNER_PHONE, "name": "Chủ quán",
            "salt": salt, "password_hash": hash_password(OWNER_PASSWORD, salt),
        })
        save_json(USERS_FILE, users)
        print(f"Da tao tai khoan chu quan mac dinh: {OWNER_PHONE} / {OWNER_PASSWORD}")
        return True


def public_order(o):
    """Ban sao cua don hang de tra ve qua API — loai bo hash cua ma huy don."""
    return {k: v for k, v in o.items() if k != "cancel_token_hash"}


def order_text(order):
    lines = []
    lines.append("=" * 40)
    lines.append(f"ĐƠN HÀNG #{order['id']}")
    lines.append(f"Thời gian: {order['created_at']}")
    lines.append(f"Khách: {order['name']}" + (f" - {order['phone']}" if order.get("phone") else ""))
    if order.get("address"):
        lines.append(f"Địa chỉ: {order['address']}")
    if order.get("method"):
        lines.append(f"Hình thức: {order['method']}")
    if order.get("time"):
        lines.append(f"Giờ muốn nhận món: {order['time']}")
    for it in order["items"]:
        lines.append(f"- {it['name']} x{it['qty']} = {fmt(it['price'] * it['qty'])}")
    lines.append(f"Tổng tiền: {fmt(order['total'])}")
    if order.get("note"):
        lines.append(f"Ghi chú: {order['note']}")
    lines.append(f"Trạng thái: {STATUS_LABEL.get(order['status'], order['status'])}")
    lines.append("=" * 40)
    return "\n".join(lines)


class Handler(BaseHTTPRequestHandler):
    # An phien ban may chu that (khong lo Python/BaseHTTP version ra header Server).
    server_version = "MayChu"
    sys_version = ""

    def version_string(self):
        # Mac dinh BaseHTTPRequestHandler ghep "MayChu " + "" (them khoang
        # trang thua); tra ve dung "MayChu" cho sach.
        return "MayChu"

    # --- helpers ---
    def _send_security_headers(self):
        for k, v in SECURITY_HEADERS.items():
            self.send_header(k, v)

    def send_json(self, code, obj, extra_headers=None):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self._send_security_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = 0
        if length <= 0:
            return {}
        if length > MAX_BODY_SIZE:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return None

    def auth_phone(self):
        auth = self.headers.get("Authorization") or ""
        if auth.startswith("Bearer "):
            return TOKENS.get(auth[7:].strip())
        return None

    def log_message(self, *args):
        # Ghi log gon nhe ra console
        print(f"[{now_vn().strftime('%H:%M:%S')}] {args[0] % args[1:] if len(args) > 1 else args[0]}")

    # --- static ---
    def do_GET(self):
        ip = client_ip(self)
        if self.path in ("/", "/index.html"):
            # Chan spam refresh: cung 1 IP tai trang qua 30 lan/phut -> 429
            # kem code captcha_required de trinh duyet mo hop thoai xac minh
            # thay vi chi bao loi. IP da qua captcha thi duoc mien.
            if not captcha_bypass_active(ip) and rate_limited(ip, "page"):
                # TRANG KHONG BAO GIO TRA JSON: neu tra JSON 429 thi trinh
                # duyet se hien trang JSON tho, nguoi dung khong bao gio
                # thay duoc captcha. Tra ve trang HTML day du (status 429)
                # kem co __NEED_CAPTCHA__ de trang tu mo captcha keo ngay
                # khi tai xong.
                log_block(ip, "tai lai trang qua nhanh -> / (tra HTML + captcha)")
                path = os.path.join(BASE_DIR, "index.html")
                with open(path, "rb") as f:
                    body = f.read()
                flag = b"<script>window.__NEED_CAPTCHA__=true;</script>"
                body = body.replace(b"</head>", flag + b"</head>", 1)
                self.send_response(429)
                self._send_security_headers()
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Retry-After", "60")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            path = os.path.join(BASE_DIR, "index.html")
            with open(path, "rb") as f:
                body = f.read()
            self.send_response(200)
            self._send_security_headers()
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/api/menu":
            # Chan spam goi thuc don lien tuc; dong thoi cap ma phien dat hang
            # (ma nay bat buoc phai kem theo khi POST /api/order).
            if not captcha_bypass_active(ip) and rate_limited(ip, "menu"):
                log_block(ip, "goi /api/menu qua nhanh")
                self.send_json(429, {"ok": False, "code": "captcha_required",
                                     "error": "Bạn tải lại trang quá nhanh, vui lòng xác minh bạn là người thật rồi thử lại"},
                              extra_headers={"Retry-After": "60"})
                return
            self.send_json(200, {"ok": True, "menu": MENU, "order_token": issue_order_token(ip)})
            return
        if self.path == "/api/captcha":
            # Cap thu thach captcha keo (nen co cho trong + manh ghep).
            # Gioi han 30 lan/IP/phut de bot khong lay ma lien tuc.
            if rate_limited(ip, "captcha"):
                log_block(ip, "lay captcha qua nhanh")
                self.send_json(429, {"ok": False,
                                     "error": "Bạn lấy mã xác minh quá nhanh, vui lòng chờ một chút rồi thử lại"},
                              extra_headers={"Retry-After": "60"})
                return
            cid, bg, piece = issue_captcha(ip)
            self.send_json(200, {"ok": True, "captcha_id": cid, "bg_svg": bg,
                                 "piece_svg": piece, "piece_w": CAPTCHA_PIECE_W,
                                 "piece_h": CAPTCHA_PIECE_H, "piece_y": CAPTCHA_GAP_Y,
                                 "track_w": CAPTCHA_BG_W})
            return
        if self.path == "/api/orders":
            phone = self.auth_phone()
            if not phone:
                self.send_json(401, {"ok": False, "error": "Chưa đăng nhập"})
                return
            orders = load_json(ORDERS_FILE, [])
            if norm_phone(phone) == OWNER_PHONE:
                visible = orders
            else:
                visible = [o for o in orders if norm_phone(o["phone"]) == norm_phone(phone)]
            visible = [public_order(o) for o in reversed(visible)]  # don moi nhat len dau
            self.send_json(200, {"ok": True, "orders": visible, "is_owner": norm_phone(phone) == OWNER_PHONE})
            return
        # Duong dan la: API thi tra JSON 404 nhu cu; duong dan thuong (nguoi
        # dung go sai URL tren trinh duyet) thi tra ve trang HTML de khong
        # bao gio hien trang JSON tho.
        if self.path.startswith("/api/"):
            self.send_json(404, {"ok": False, "error": "Không tìm thấy"})
            return
        path = os.path.join(BASE_DIR, "index.html")
        with open(path, "rb") as f:
            body = f.read()
        self.send_response(404)
        self._send_security_headers()
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        ip = client_ip(self)
        # 1. Chan body qua lon truoc khi doc (64KB).
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = 0
        if length > MAX_BODY_SIZE:
            log_block(ip, f"body qua lon ({length} bytes) -> {self.path}")
            self.send_json(413, {"ok": False, "error": "Dữ liệu gửi lên quá lớn, vui lòng thử lại"})
            return
        # 2. Gioi han tan suat theo IP tren tung endpoint ghi.
        # Rieng /api/order: kiem tra trong handler (sau khi doc JSON) de
        # biet duoc captcha_pass — IP da qua captcha duoc mien gioi han.
        rate_key = {
            "/api/order": "order", "/api/login": "login", "/api/register": "register",
        }.get(self.path, "other")
        if self.path != "/api/order" and rate_limited(ip, rate_key):
            log_block(ip, f"vuot gioi han tan suat ({rate_key}) -> {self.path}")
            self.send_json(429, {"ok": False, "error": "Bạn thao tác quá nhanh, vui lòng chờ một chút rồi thử lại"},
                          extra_headers={"Retry-After": "60"})
            return
        # 3. API POST chi nhan JSON.
        if length > 0:
            ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            if ctype != "application/json":
                self.send_json(415, {"ok": False, "error": "Dữ liệu gửi lên phải là JSON"})
                return
        data = self.read_json()
        if data is None:
            self.send_json(400, {"ok": False, "error": "Body phải là JSON"})
            return
        if not isinstance(data, dict):
            self.send_json(400, {"ok": False, "error": "Body phải là JSON object"})
            return

        if self.path == "/api/register":
            phone = norm_phone(data.get("phone"))
            name = clean_text(data.get("name"), MAX_NAME_LEN + 1)
            password = str(data.get("password") or "")
            if len(phone) < 9 or len(phone) > 11 or not phone.startswith("0"):
                self.send_json(400, {"ok": False, "error": "Số điện thoại không hợp lệ (vd: 0358961119)"})
                return
            if not name:
                self.send_json(400, {"ok": False, "error": "Vui lòng nhập tên"})
                return
            if len(name) > MAX_NAME_LEN:
                self.send_json(400, {"ok": False, "error": f"Tên quá dài (tối đa {MAX_NAME_LEN} ký tự)"})
                return
            if len(password) < 4 or len(password) > 100:
                self.send_json(400, {"ok": False, "error": "Mật khẩu từ 4 đến 100 ký tự"})
                return
            with LOCK:
                users = load_json(USERS_FILE, [])
                if any(norm_phone(u["phone"]) == phone for u in users):
                    self.send_json(400, {"ok": False, "error": "Số điện thoại này đã đăng ký"})
                    return
                salt = secrets.token_hex(16)
                users.append({
                    "phone": phone, "name": name,
                    "salt": salt, "password_hash": hash_password(password, salt),
                })
                save_json(USERS_FILE, users)
            self.send_json(200, {"ok": True, "message": "Đăng ký thành công, mời đăng nhập"})
            return

        if self.path == "/api/login":
            phone = norm_phone(data.get("phone"))
            password = str(data.get("password") or "")
            # Khoa SDT khi doan sai qua nhieu lan: 5 lan sai trong 10 phut
            # -> khoa 15 phut (429). Kiem tra truoc khi doi mat khau.
            locked, retry_s = login_locked(phone)
            if locked:
                log_block(ip, f"SDT {phone} dang bi khoa dang nhap (con {retry_s}s)")
                self.send_json(429, {"ok": False, "error": "Tài khoản này tạm khóa 15 phút do đăng nhập sai nhiều lần, vui lòng thử lại sau"},
                              extra_headers={"Retry-After": str(retry_s)})
                return
            if len(password) > 100:
                record_login_failure(phone)
                self.send_json(401, {"ok": False, "error": "Số điện thoại hoặc mật khẩu sai"})
                return
            ensure_owner_account()  # phong khi users.json bi mat ma may chu chua khoi dong lai
            users = load_json(USERS_FILE, [])
            user = next((u for u in users if norm_phone(u["phone"]) == phone), None)
            if not user or hash_password(password, user["salt"]) != user["password_hash"]:
                record_login_failure(phone)
                self.send_json(401, {"ok": False, "error": "Số điện thoại hoặc mật khẩu sai"})
                return
            clear_login_failures(phone)  # dang nhap dung: xoa lich su sai
            token = secrets.token_hex(16)
            TOKENS[token] = phone
            self.send_json(200, {
                "ok": True, "token": token,
                "user": {"phone": phone, "name": user["name"], "is_owner": phone == OWNER_PHONE},
            })
            return

        if self.path == "/api/order":
            # Dat hang CHI CAN TEN - khong can dang nhap, khong can SDT / dia chi.
            # Neu khach da dang nhap thi lay SDT/tai khoan neu co, khong bat buoc.
            phone = self.auth_phone() or ""
            # Bypass captcha: IP da qua xac minh (kem captcha_pass hop le
            # hoac dang co bypass token con han) duoc mien gioi han tan
            # suat dat don va cooldown 3 giay. Cac check khac (order_token,
            # honeypot, min-time, gioi han so luong) VAN ap dung day du.
            bypass_ok = valid_captcha_bypass(data.get("captcha_pass"), ip) or captcha_bypass_active(ip)
            # Chong spam: moi IP toi da 10 don/phut. Vuot qua -> 429 kem code
            # captcha_required de trinh duyet mo hop thoai xac minh.
            if not bypass_ok and rate_limited(ip, "order"):
                log_block(ip, "vuot gioi han dat don (10/phut) -> /api/order")
                self.send_json(429, {"ok": False, "code": "captcha_required",
                                     "error": "Bạn đặt đơn quá nhanh, vui lòng xác minh bạn là người thật rồi thử lại"},
                              extra_headers={"Retry-After": "60"})
                return
            # Ma phien dat hang: bat buoc phai lay tu GET /api/menu truoc
            # (gan voi IP, han 10 phut). Bot POST thang khong co ma -> 403.
            # Frontend gap loi nay se tu lay ma moi roi gui lai 1 lan.
            order_token = data.get("order_token")
            if not valid_order_token(order_token, ip):
                log_block(ip, "don khong co ma phien hop le -> /api/order")
                self.send_json(403, {"ok": False, "code": "order_token_expired",
                                     "error": "Phiên đặt hàng đã hết hạn, vui lòng tải lại trang rồi đặt lại"})
                return
            # Chong bot: honeypot — o "website" an tren form, nguoi that luon de
            # trong; bot dien vao thi bi chan (tra loi chung chung de khong lo).
            if str(data.get("website") or "").strip():
                log_block(ip, "honeypot co gia tri -> /api/order")
                self.send_json(400, {"ok": False, "error": "Đặt hàng thất bại, vui lòng thử lại"})
                return
            # Chong bot: don gui qua nhanh sau khi mo trang (< 0.8 giay).
            try:
                form_time = int(data.get("form_time_ms"))
            except Exception:
                form_time = None
            if form_time is not None and form_time < MIN_FORM_TIME_MS:
                log_block(ip, f"don gui qua nhanh ({form_time}ms) -> /api/order")
                self.send_json(400, {"ok": False, "error": "Đặt hàng thất bại, vui lòng thử lại"})
                return
            name = clean_text(data.get("name"), MAX_NAME_LEN + 1)
            if not name and phone:
                users = load_json(USERS_FILE, [])
                user = next((u for u in users if norm_phone(u["phone"]) == norm_phone(phone)), None)
                if user:
                    name = user["name"]
            if not name:
                self.send_json(400, {"ok": False, "error": "Vui lòng nhập tên khách hàng"})
                return
            if len(name) > MAX_NAME_LEN:
                self.send_json(400, {"ok": False, "error": f"Tên quá dài (tối đa {MAX_NAME_LEN} ký tự)"})
                return
            # Chong spam: cung 1 IP / cung 1 ten vua dat don xong thi phai doi 3 giay.
            # IP da qua captcha duoc mien. Vuot qua -> 429 kem code de mo captcha.
            if not bypass_ok and order_cooldown_active(ip, name):
                log_block(ip, f"don cach nhau < {ORDER_COOLDOWN_S}s (ten: {name})")
                self.send_json(429, {"ok": False, "code": "captcha_required",
                                     "error": "Bạn vừa đặt đơn, vui lòng xác minh bạn là người thật rồi đặt tiếp"},
                              extra_headers={"Retry-After": "3"})
                return
            items_in = data.get("items") or []
            address = clean_text(data.get("address"), MAX_ADDRESS_LEN)  # tuy chon
            note = clean_text(data.get("note"), MAX_NOTE_LEN)
            method = clean_text(data.get("method") or data.get("delivery"), MAX_METHOD_LEN)
            time = clean_text(data.get("time") or data.get("delivery_time"), MAX_TIME_LEN)
            if not isinstance(items_in, list) or not items_in:
                self.send_json(400, {"ok": False, "error": "Giỏ hàng đang trống"})
                return
            if len(items_in) > MAX_ITEMS_PER_ORDER:
                self.send_json(400, {"ok": False, "error": f"Mỗi đơn tối đa {MAX_ITEMS_PER_ORDER} món"})
                return
            items, total, total_qty = [], 0, 0
            for raw in items_in:
                if not isinstance(raw, dict):
                    continue
                try:
                    mid, qty = int(raw.get("id")), int(raw.get("qty"))
                except Exception:
                    continue
                if mid not in MENU_BY_ID or qty < 1 or qty > MAX_QTY_PER_DISH:
                    continue
                total_qty += qty
                if total_qty > MAX_ITEMS_PER_ORDER:
                    self.send_json(400, {"ok": False, "error": f"Mỗi đơn tối đa {MAX_ITEMS_PER_ORDER} món"})
                    return
                m = MENU_BY_ID[mid]
                items.append({"id": mid, "name": m["name"], "price": m["price"], "qty": qty})
                total += m["price"] * qty
            if not items:
                self.send_json(400, {"ok": False, "error": "Món chọn không hợp lệ"})
                return
            # Ma huy don: chi khach dat don nay moi co (tra ve 1 lan duy nhat).
            # May chu chi luu SHA-256 cua ma, khong luu ma goc.
            cancel_token = secrets.token_hex(16)
            with LOCK:
                orders = load_json(ORDERS_FILE, [])
                order_id = (max([o["id"] for o in orders], default=0) + 1)
                order = {
                    "id": order_id,
                    "created_at": now_vn().strftime("%d/%m/%Y %H:%M:%S"),
                    "phone": phone, "name": name, "address": address,
                    "method": method, "time": time,
                    "note": note, "items": items, "total": total, "status": "moi",
                    "cancel_token_hash": hashlib.sha256(cancel_token.encode("utf-8")).hexdigest(),
                }
                order["text"] = order_text(order)
                orders.append(order)
                save_json(ORDERS_FILE, orders)
                with open(ORDERS_TXT, "a", encoding="utf-8") as f:
                    f.write(order["text"] + "\n\n")
            mark_order_success(ip, name)  # bat dau dem cooldown 3 giay cho IP/ten nay
            # Ma phien chi dung duoc cho 1 don thanh cong -> xoa ngay.
            if isinstance(order_token, str):
                with _order_token_lock:
                    _order_tokens.pop(order_token, None)
            print(f"ĐƠN MỚI #{order_id} - {name} ({phone}) - {fmt(total)}")
            self.send_json(200, {"ok": True, "order_id": order_id, "total": total,
                                 "order_text": order["text"], "cancel_token": cancel_token})
            return

        if self.path == "/api/order/cancel":
            # Khach huy don cua minh. Khong can dang nhap: dung ma huy don
            # (cancel_token) tra ve luc dat don. Khach da dang nhap cung co
            # the huy don cua minh (hoac chu quan huy bat ky don nao) bang
            # token dang nhap, khong can ma huy.
            try:
                oid = int(data.get("id"))
            except Exception:
                self.send_json(400, {"ok": False, "error": "Thiếu mã đơn"})
                return
            token = str(data.get("token") or data.get("cancel_token") or "")
            caller = self.auth_phone()
            with LOCK:
                orders = load_json(ORDERS_FILE, [])
                order = next((o for o in orders if o["id"] == oid), None)
                if not order:
                    self.send_json(404, {"ok": False, "error": "Không tìm thấy đơn"})
                    return
                if order.get("status") != "moi":
                    self.send_json(400, {"ok": False, "error": "Chỉ hủy được đơn đang ở trạng thái Mới"})
                    return
                allowed = False
                if caller and norm_phone(caller) == OWNER_PHONE:
                    allowed = True
                elif caller and norm_phone(order.get("phone")) and norm_phone(order.get("phone")) == norm_phone(caller):
                    allowed = True
                elif token and order.get("cancel_token_hash"):
                    if hashlib.sha256(token.encode("utf-8")).hexdigest() == order["cancel_token_hash"]:
                        allowed = True
                if not allowed:
                    self.send_json(403, {"ok": False, "error": "Mã hủy không đúng hoặc bạn không có quyền hủy đơn này"})
                    return
                orders = [o for o in orders if o["id"] != oid]
                save_json(ORDERS_FILE, orders)
                with open(ORDERS_TXT, "w", encoding="utf-8") as f:
                    f.write("DANH SÁCH ĐƠN HÀNG - XÔI BÁNH MÌ DRINK\n")
                    for o in orders:
                        f.write((o.get("text") or order_text(o)) + "\n\n")
            print(f"KHÁCH ĐÃ HỦY ĐƠN #{oid} - {order.get('name')} - {fmt(order.get('total', 0))}")
            self.send_json(200, {"ok": True, "message": f"Đã hủy đơn #{oid}"})
            return

        if self.path == "/api/order/delete":
            phone = self.auth_phone()
            if not phone:
                self.send_json(401, {"ok": False, "error": "Vui lòng đăng nhập trước khi xóa đơn"})
                return
            try:
                oid = int(data.get("id"))
            except Exception:
                self.send_json(400, {"ok": False, "error": "Thiếu mã đơn"})
                return
            with LOCK:
                orders = load_json(ORDERS_FILE, [])
                order = next((o for o in orders if o["id"] == oid), None)
                if not order:
                    self.send_json(404, {"ok": False, "error": "Không tìm thấy đơn"})
                    return
                is_owner = norm_phone(phone) == OWNER_PHONE
                if not is_owner:
                    # Khach chi xoa duoc don cua chinh minh va chi khi don con o trang thai "Moi".
                    if not norm_phone(order.get("phone")) or norm_phone(order.get("phone")) != norm_phone(phone):
                        self.send_json(403, {"ok": False, "error": "Bạn chỉ được xóa đơn của mình"})
                        return
                    if order.get("status") != "moi":
                        self.send_json(403, {"ok": False, "error": "Chỉ xóa được đơn đang ở trạng thái Mới"})
                        return
                orders = [o for o in orders if o["id"] != oid]
                save_json(ORDERS_FILE, orders)
                # Viet lai don-hang.txt tu cac don con lai de file luon khop voi orders.json.
                with open(ORDERS_TXT, "w", encoding="utf-8") as f:
                    f.write("DANH SÁCH ĐƠN HÀNG - XÔI BÁNH MÌ DRINK\n")
                    for o in orders:
                        f.write((o.get("text") or order_text(o)) + "\n\n")
            print(f"ĐÃ XÓA ĐƠN #{oid} - {order.get('name')} - {fmt(order.get('total', 0))}")
            self.send_json(200, {"ok": True, "message": f"Đã xóa đơn #{oid}"})
            return

        if self.path == "/api/order/status":
            phone = self.auth_phone()
            if not phone or norm_phone(phone) != OWNER_PHONE:
                self.send_json(403, {"ok": False, "error": "Chỉ chủ quán mới đổi được trạng thái đơn"})
                return
            try:
                oid = int(data.get("id"))
            except Exception:
                self.send_json(400, {"ok": False, "error": "Thiếu mã đơn"})
                return
            status = str(data.get("status") or "")
            if status not in ("xac-nhan", "hoan-thanh", "huy"):
                self.send_json(400, {"ok": False, "error": "Trạng thái không hợp lệ"})
                return
            with LOCK:
                orders = load_json(ORDERS_FILE, [])
                order = next((o for o in orders if o["id"] == oid), None)
                if not order:
                    self.send_json(404, {"ok": False, "error": "Không tìm thấy đơn"})
                    return
                order["status"] = status
                order["text"] = order_text(order)
                save_json(ORDERS_FILE, orders)
            self.send_json(200, {"ok": True, "message": "Đã cập nhật trạng thái"})
            return

        if self.path == "/api/captcha/verify":
            # Xac minh vi tri keo cua captcha puzzle: manh ghep phai nam
            # trong ±6px so voi cho trong. Dung thi tra bypass token 10
            # phut (gan voi IP); sai qua 5 lan thi huy ma.
            cid = str(data.get("captcha_id") or "")
            http_code, err_code, msg_text, token = verify_captcha(
                cid, data.get("offset"), ip)
            if http_code != 200:
                self.send_json(http_code, {"ok": False, "code": err_code, "error": msg_text})
                return
            self.send_json(200, {"ok": True, "message": msg_text, "bypass_token": token})
            return

        self.send_json(404, {"ok": False, "error": "Không tìm thấy"})


if __name__ == "__main__":
    for path, default in ((USERS_FILE, []), (ORDERS_FILE, [])):
        if not os.path.exists(path):
            save_json(path, default)
    ensure_owner_account()  # tai khoan chu quan mac dinh: 0358961119 / quan2026
    if not os.path.exists(ORDERS_TXT):
        with open(ORDERS_TXT, "w", encoding="utf-8") as f:
            f.write("DANH SÁCH ĐƠN HÀNG - XÔI BÁNH MÌ DRINK\n")
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print("=" * 55)
    print("QUÁN XÔI - BÁNH MÌ - DRINK  |  Máy chủ đang chạy")
    print(f"Mở Chrome:  http://localhost:{PORT}")
    print("Tren Render: mo link https://<ten-dich-vu>.onrender.com ma Render cap")
    print("Đơn hàng lưu vào: don-hang.txt (ngay trong thư mục này)")
    print("Nhấn Ctrl+C để dừng máy chủ.")
    print("=" * 55)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng máy chủ.")
