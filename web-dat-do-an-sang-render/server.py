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
import os
import secrets
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
    # --- helpers ---
    def send_json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
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
        if self.path in ("/", "/index.html"):
            path = os.path.join(BASE_DIR, "index.html")
            with open(path, "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/api/menu":
            self.send_json(200, {"ok": True, "menu": MENU})
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
        self.send_json(404, {"ok": False, "error": "Không tìm thấy"})

    def do_POST(self):
        data = self.read_json()
        if data is None:
            self.send_json(400, {"ok": False, "error": "Body phải là JSON"})
            return

        if self.path == "/api/register":
            phone = norm_phone(data.get("phone"))
            name = str(data.get("name") or "").strip()
            password = str(data.get("password") or "")
            if len(phone) < 9 or len(phone) > 11 or not phone.startswith("0"):
                self.send_json(400, {"ok": False, "error": "Số điện thoại không hợp lệ (vd: 0358961119)"})
                return
            if not name:
                self.send_json(400, {"ok": False, "error": "Vui lòng nhập tên"})
                return
            if len(password) < 4:
                self.send_json(400, {"ok": False, "error": "Mật khẩu ít nhất 4 ký tự"})
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
            ensure_owner_account()  # phong khi users.json bi mat ma may chu chua khoi dong lai
            users = load_json(USERS_FILE, [])
            user = next((u for u in users if norm_phone(u["phone"]) == phone), None)
            if not user or hash_password(password, user["salt"]) != user["password_hash"]:
                self.send_json(401, {"ok": False, "error": "Số điện thoại hoặc mật khẩu sai"})
                return
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
            name = str(data.get("name") or "").strip()
            if not name and phone:
                users = load_json(USERS_FILE, [])
                user = next((u for u in users if norm_phone(u["phone"]) == norm_phone(phone)), None)
                if user:
                    name = user["name"]
            if not name:
                self.send_json(400, {"ok": False, "error": "Vui lòng nhập tên khách hàng"})
                return
            items_in = data.get("items") or []
            address = str(data.get("address") or "").strip()  # tuy chon
            note = str(data.get("note") or "").strip()
            method = str(data.get("method") or data.get("delivery") or "").strip()
            time = str(data.get("time") or data.get("delivery_time") or "").strip()
            if not isinstance(items_in, list) or not items_in:
                self.send_json(400, {"ok": False, "error": "Giỏ hàng đang trống"})
                return
            items, total = [], 0
            for raw in items_in:
                try:
                    mid, qty = int(raw.get("id")), int(raw.get("qty"))
                except Exception:
                    continue
                if mid not in MENU_BY_ID or qty < 1 or qty > 99:
                    continue
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
