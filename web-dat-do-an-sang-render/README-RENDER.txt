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
  - Mo link tren, vao tab "Tai khoan" -> "Dang ky" bang so 0358961119 truoc (1 lan duy nhat),
    dat mat khau (nho mat khau nay), roi "Dang nhap" bang so do.
  - Vao tab "Quan - Don moi": don moi tu hien sau toi da 5 giay, co tieng "bip",
    bam Xac nhan / Hoan thanh / Huy. Nut "Xuat tat ca don (.txt)" de tai toan bo don ve may.
  - XOA DON: moi the don co nut "Xoa don" (chu quan thay tren moi don). Bam vao,
    xac nhan ma don + tong tien, don se bi xoa vinh vien khoi may chu (ca orders.json
    va don-hang.txt). Khach dang nhap chi xoa duoc don cua chinh minh khi don con
    o trang thai "Moi"; khach khong dang nhap khong xoa duoc don.
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
    Tai khoan chu quan (so 0358961119) neu mat thi dang ky lai nhu Buoc 5.
  - Ban host tren Render nay KHONG gui don ve Muse. Don chi nam tren may chu Render.
    Muon Muse bao don moi thi van dung ban web dong trong Muse nhu truoc.
  - Khach van co the gui them don qua SMS / Zalo ve so 0355368270 bang nut tren web.
