DUA WEB DAT DO AN SANG LEN HOST ONLINE FREE (RENDER)
Quan: Xoi - Banh mi - Drink | So 61, ngo 54 Le Quang Dao, Phu Do, Tu Liem, Ha Noi
So quan: 0358.96.1119 | Nhan don qua SMS/Zalo: 0355368270
Khach dat hang CHI CAN TEN, khong can dang nhap, khong can SDT hay dia chi.

BUOC 1 - TAO TAI KHOAN RENDER (MIEN PHI)
  - Mo https://render.com , bam "Get Started", dang ky bang email hoac tai khoan GitHub.
  - Khong can nhap the ngan hang cho goi Free.

BUOC 2 - DUA CODE LEN GITHUB
  - Mo https://github.com , dang nhap (hoac tao tai khoan mien phi), bam "New repository",
    dat ten vi du: web-dat-do-an-sang , chon Public, bam "Create repository".
  - Tai len tat ca file trong thu muc nay (server.py, index.html, render.yaml,
    requirements.txt, README-RENDER.txt) bang nut "uploading an existing file".
  - Khong can tai len users.json / orders.json / don-hang.txt (may chu se tu tao).

BUOC 3 - TAO WEB SERVICE TREN RENDER
  - Vao https://dashboard.render.com , bam "New +" -> "Web Service".
  - Chon "Build and deploy from a Git repository", chon repo vua tao o Buoc 2.
  - Dat ten (Name): web-dat-do-an-sang (ten nay se thanh link ...onrender.com).
  - Region: chon Singapore (gan Viet Nam nhat).
  - Runtime: Python 3. Branch: main (hoac master, tuy repo cua ban).
  - Build Command: de trong (hoac giu nguyen nhu trong render.yaml).
  - Start Command: python server.py
  - Instance Type: Free.
  - Bam "Create Web Service" va doi vai phut cho Render build xong.

BUOC 4 - LAY LINK VA GUI CHO MOI NGUOI
  - Link cua ban se co dang: https://web-dat-do-an-sang.onrender.com
    (ten chinh xac hien o tren cung trang Web Service cua ban tren Render).
  - Gui link nay cho khach: ai cung mo duoc, chon mon, chi can nhap ten roi bam
    "Ban don ve quan". Don luu ngay tren may chu Render.

BUOC 5 - CHU QUAN XEM DON
  - TAI KHOAN CHU QUAN MAC DINH (da co san, khong can dang ky): so 0358961119,
    mat khau quan2026. Mo link tren, vao tab "Tai khoan" -> "Dang nhap" bang so
    va mat khau nay la xong. Ke ca sau khi Render deploy lai lam mat users.json,
    may chu se tu tao lai tai khoan nay khi khoi dong, dang nhap ngay duoc.
  - TAB "QUAN - DON MOI" CHI HIEN VOI CHU QUAN: khach va tai khoan khong phai
    chu quan khong thay tab nay tren thanh dieu huong, khong thay noi dung don
    cua quan. Chi khi dang nhap dung so 0358961119 tab moi hien ra.
  - Vao tab "Quan - Don moi": don moi tu hien sau toi da 5 giay, co tieng "bip",
    bam Xac nhan / Hoan thanh / Huy. Nut "Xuat tat ca don (.txt)" de tai toan bo don ve may.
  - XOA DON: moi the don co nut "Xoa don" (chu quan thay tren moi don, ca o tab
    "Don cua toi" va tab "Quan - Don moi"). Bam vao, xac nhan ma don + tong tien,
    don se bi xoa vinh vien khoi may chu (ca orders.json va don-hang.txt).
    Khach dang nhap chi xoa duoc don cua chinh minh khi don con o trang thai "Moi".
  - KHACH HUY DON: khach dat don chi can ten (khong can dang nhap) van huy duoc
    don cua minh khi don con o trang thai "Moi": tren the don vua dat xong co nut
    "Huy don nay", va tren the don trong tab "Don cua toi" co nut "Huy don".
    Khach chi huy duoc don cua chinh minh (nho ma huy luu tren trinh duyet luc dat don).
  - THONG BAO HUY DON CHO CHU QUAN: khi khach huy don, don se tu bien mat khoi
    tab "Quan - Don moi" trong vong 5 giay (khong can tai lai trang), dong thoi
    hien bang thong bao "Don #... vua bi huy boi khach" kem gio Viet Nam va keu
    "bip". Luu toi da 5 thong bao gan nhat, moi nhat len dau.
  - CAP NHAT REALTIME: ca tab "Don cua toi" (khach xem don cua minh) va tab
    "Quan - Don moi" (chu quan xem tat ca don) deu tu lam moi moi 5 giay khi
    dang mo tab don, khong can bam "Tai lai" hay tai lai trang. Don moi xuat
    hien se duoc to do va keu "bip". Khi an tab trinh duyet (chuyen sang tab
    khac), viec tu lam moi tam dung de tiet kiem tai nguyen; mo lai tab thi
    lam moi ngay lap tuc.

LUU Y QUAN TRONG - NOI THAT
  - Goi Free cua Render se "ngu" sau khoang 15 phut khong co ai mo web. Lan mo dau tien
    sau khi ngu co the mat khoang 1 phut moi len web. Mo lai lan 2 la nhanh ngay.
  - O cung cua goi Free la tam thoi (ephemeral): khi Render khoi dong lai may chu hoac
    ban deploy lai code moi, file orders.json / don-hang.txt / users.json co the MAT.
    Hay thuong xuyen bam "Xuat tat ca don (.txt)" de tai don ve may, nhat la cuoi ngay.
    Tai khoan chu quan mac dinh (0358961119 / quan2026) se tu duoc tao lai khi may
    chu khoi dong, nen khong can dang ky lai.
  - Ban host tren Render nay KHONG gui don ve Muse. Don chi nam tren may chu Render.
    Muon Muse bao don moi thi van dung ban web dong trong Muse nhu truoc.
  - Khach van co the gui them don qua SMS / Zalo ve so 0355368270 bang nut tren web.

GIAO DIỆN MỚI (bản cao cấp):
- Banner đầu trang gradient vàng-cam, nút gọi/Zalo bấm được ngay.
- Mỗi món có icon riêng (trứng, chả, bò khô, trà chanh...), lưới 2 cột trên máy tính, 1 cột trên điện thoại; pill nhóm món có kèm số lượng món.
- Thanh giỏ hàng nổi hình viên thuốc ở cuối màn hình, nút "Bắn đơn về quán" to, gradient vàng.
- Thẻ đơn hiển thị đầy đủ: tên khách, giờ (giờ VN), hình thức/giờ nhận, ghi chú, từng món 1 dòng (tên × số lượng — đơn giá = thành tiền), tổng tiền to, huy hiệu trạng thái.
- Tab "Quán - Đơn mới" (chỉ chủ quán): nút "📊 Xuất file tổng" tải file tong-hop-don-YYYYMMDD-HHmm.txt gồm tổng đơn, tổng doanh thu, đếm theo trạng thái, doanh thu theo từng món (cao → thấp), rồi chi tiết đầy đủ từng đơn. Nút "Xuất tất cả đơn (.txt)" cũ vẫn còn.

UI/UX MƯỢT MÀ HƠN + CHỐNG SPAM + BẢO MẬT (bản cập nhật 07/11/2026):
- UI mượt hơn: chuyển cảnh mờ dần khi đổi tab, thanh giỏ nảy nhẹ khi thêm món,
  nút bấm có phản hồi, tìm món debounce 200ms (gõ nhanh không giật), skeleton
  loading khi đang tải thực đơn, cuộn mượt, tôn trọng chế độ "giảm chuyển động"
  của điện thoại. Vẫn chỉ dùng font hệ thống, không tải thêm gì nên web nhẹ như cũ.
- Chống bấm 2 lần: nút "Bắn đơn về quán" tự khóa trong lúc đang gửi đơn
  (hiện "Đang gửi đơn…"), tránh double-tap tạo 2 đơn trùng.
- Chống spam (máy chủ): mỗi IP tối đa 10 lần đặt đơn / 10 lần đăng nhập /
  5 lần đăng ký trong 1 phút, vượt quá trả lỗi 429 "Bạn thao tác quá nhanh...";
  2 đơn liên tiếp từ cùng 1 IP hoặc cùng 1 tên phải cách nhau ít nhất 3 giây;
  ô honeypot ẩn + đơn gửi dưới 0.8 giây sau khi mở trang bị chặn (chống bot);
  mỗi đơn tối đa 20 món, mỗi món tối đa 10 phần; tên tối đa 50 ký tự.
  Khách đặt bình thường (vài giây 1 đơn) không bị ảnh hưởng. Lần chặn nào
  máy chủ cũng ghi log "CHẶN" kèm lý do để chủ quán kiểm tra.
- Bảo mật: mọi phản hồi đều có header X-Content-Type-Options, X-Frame-Options
  (chống nhúng web vào iframe lạ), Referrer-Policy, Content-Security-Policy
  (chỉ cho tải từ chính web này), Permissions-Policy; giới hạn body 64KB
  (quá lớn trả 413), API POST chỉ nhận JSON (sai định dạng trả 415);
  mọi chữ khách nhập (tên, ghi chú...) đều được lọc ký tự lạ và giới hạn độ dài,
  khi hiển thị đều escape để không chèn được mã HTML; header Server không còn
  lộ phiên bản Python; mật khẩu vẫn mã hóa PBKDF2, mã hủy đơn vẫn chỉ lưu
  dạng SHA-256 như trước.

CHẶN SPAM REFRESH + BẢO MẬT THÊM (bản cập nhật 07/11/2026):
- Chặn spam refresh (trình duyệt): mỗi tab đếm số lần tải trang trong 10 giây,
  quá 5 lần thì hiện màn hình chờ toàn trang "Bạn tải lại trang quá nhanh"
  kèm đếm ngược, hết giờ mới cho dùng tiếp (giỏ hàng vẫn giữ nguyên).
  Tải lại 1-2 lần bình thường không bao giờ bị chặn. Cảnh báo beforeunload
  cũ (hỏi trước khi tải lại lúc giỏ đang có món) vẫn giữ nguyên.
- Chặn spam refresh (máy chủ): cùng 1 IP tải trang hoặc gọi thực đơn quá
  30 lần/phút sẽ bị trả 429 "Bạn tải lại trang quá nhanh...". Riêng việc
  tự làm mới danh sách đơn mỗi 5 giây KHÔNG bị giới hạn nên chủ quán vẫn
  xem đơn realtime bình thường.
- Mã phiên đặt hàng: thực đơn (GET /api/menu) kèm 1 mã ngẫu nhiên, gắn với
  IP, hạn 10 phút, chỉ dùng được cho 1 đơn thành công. Đơn POST bắt buộc
  phải kèm mã này, không có mã hoặc mã sai/hết hạn sẽ bị từ chối 403.
  Nếu mã hết hạn giữa chừng, trang tự lấy mã mới rồi gửi lại đơn 1 lần
  nên khách thật không bị ảnh hưởng; bot POST thẳng không qua trang web
  sẽ luôn thất bại.
- Header bảo mật mới: Strict-Transport-Security (HSTS 1 năm), 
  Cross-Origin-Resource-Policy: same-origin, X-Permitted-Cross-Domain-Policies:
  none. Các header cũ giữ nguyên.
- Chống đoán mật khẩu: đăng nhập sai 5 lần cho cùng 1 số điện thoại trong
  10 phút thì khóa số đó 15 phút (trả 429, báo rõ bằng tiếng Việt).
  Đăng nhập đúng sẽ xóa hết lịch sử sai. Chủ quán đăng nhập đúng như
  bình thường không bị ảnh hưởng.

CAPTCHA KÉO (DRAG SLIDER PUZZLE) — NHẢY CAPTCHA KHI SPAM (bản cập nhật 07/11/2026):
- Khi máy chủ chặn spam (đặt đơn quá 10 lần/phút, 2 đơn cách nhau dưới
  3 giây, tải lại trang/thực đơn quá 30 lần/phút), thay vì chỉ báo lỗi
  429, trang sẽ NHẢY HỘP THOẠI CAPTCHA để khách xác minh mình là người
  thật rồi tự gửi lại đơn / tải lại thực đơn. Khách dùng bình thường
  (không chạm ngưỡng spam) KHÔNG BAO GIỜ thấy captcha. Đăng nhập sai
  nhiều lần vẫn khóa 15 phút như cũ, KHÔNG có captcha ở đăng nhập.
- Captcha tự xây trong máy chủ, không dùng dịch vụ ngoài, không cần
  đăng ký API key: hộp thoại hiện 1 hình nền 300x150 (gradient + hoa
  văn ngẫu nhiên) có 1 chỗ trống hình mảnh ghép ở vị trí x ngẫu nhiên,
  và 1 mảnh ghép (đúng lát cắt hoa văn của chỗ trống đó) ở mép trái.
  Người dùng KÉO NÚT TRƯỢT (chuột hoặc cảm ứng) để đưa mảnh ghép vào
  đúng chỗ trống; thả tay là gửi vị trí lên máy chủ kiểm tra.
- Vị trí đúng CHỈ lưu ở máy chủ, không bao giờ trả về trình duyệt; sai
  số cho phép ±6px. Mỗi mã chỉ cho sai tối đa 5 lần (hiển thị số lần
  còn lại), sai lần thứ 6 thì mã bị hủy, phải bấm "Đổi câu khác" lấy mã
  mới. Mã chỉ có hạn 3 phút. Qua được thì nhận bypass token 10 phút
  gắn với IP: trong 10 phút đó IP được miễn các giới hạn spam (tốc độ
  đặt đơn, cooldown 3 giây, giới hạn tải trang) nhưng vẫn phải có mã
  phiên đặt hàng, honeypot, đơn gửi đủ 0.8 giây và giới hạn số lượng
  như bình thường. Mọi lần cấp mã / kéo sai / qua / bị hủy đều ghi log
  trên máy chủ.
- API mới (máy chủ): GET /api/captcha trả {captcha_id, bg_svg, piece_svg,
  piece_w, piece_h, piece_y, track_w} (2 ảnh SVG dạng data URI, xem được
  ngay không cần tải thêm); POST /api/captcha/verify với {captcha_id,
  offset} trả 200 + bypass_token khi đúng, 400 khi sai/hết hạn (kèm mã
  lỗi captcha_wrong / captcha_expired / captcha_locked để trang tự đổi
  mã mới). Đơn POST kèm thêm trường captcha_pass (bypass token) khi có.

## Giao diện mới (07/11/2026) — xanh lá đậm + kem, giỏ hàng sidebar
- Phong cách mới: nền kem ấm, xanh lá đậm (#1B4332/#2D6A4F) + nâu gỗ, thẻ
  trắng, bóng mềm, font hệ thống, không tài nguyên ngoài. Tên quán, địa chỉ,
  chip liên hệ, tagline, badge, 4 tab điều hướng và thẻ món (icon emoji +
  gợi ý vị) giữ nguyên nội dung, chỉ đổi màu theo phong cách mới.
- Giỏ hàng dạng sidebar trượt ra từ phải (rộng 420px desktop, 94vw mobile):
  nút "Giỏ hàng" cố định góc phải trên desktop (nằm trong header trên mobile),
  hiện số món + tổng tiền. Bấm nút mở sidebar, bấm lớp mờ / nút ✕ / phím
  Escape để đóng, trượt mượt ~0.3s, khi mở sẽ khóa cuộn trang chính.
  Trong sidebar: danh sách món (tăng/giảm số lượng, thành tiền từng dòng),
  tổng tiền và form đặt hàng (tên, hình thức, giờ nhận, ghi chú) như cũ.
  Đặt đơn thành công thì sidebar tự đóng và hiện thẻ thành công ở trang chính.
- Đã bỏ thanh giỏ nổi dưới cùng. Cảnh báo beforeunload (giỏ có món / đơn
  đang gửi) và chặn spam refresh vẫn hoạt động như trước.

---
GHI CHÚ BẢN SỬA 07/11/2026 — Sửa lỗi trang JSON thô khi chặn spam tải trang:
- Trước đây: tải lại trang quá 30 lần/phút thì máy chủ trả thẳng JSON 429
  nên trình duyệt hiện nguyên trang JSON, người dùng không thấy captcha.
- Nay: GET / (và mọi đường dẫn không phải API) KHÔNG BAO GIỜ trả JSON.
  Khi chạm giới hạn tải trang, máy chủ trả về trang HTML đầy đủ (status
  429, Content-Type text/html) kèm cờ window.__NEED_CAPTCHA__=true trong
  <head>; trang vừa tải xong sẽ tự mở ngay hộp thoại captcha kéo, qua
  xác minh thì xóa bộ đếm spam refresh ở trình duyệt rồi tải thực đơn
  bình thường. API (/api/menu, /api/order...) vẫn trả JSON 429 như cũ để
  code cũ xử lý. Đường dẫn lạ không phải API cũng trả về trang HTML.
