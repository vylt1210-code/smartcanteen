# UTH Smart Canteen — Full Python Prototype

## 1. Cài đặt

Python 3.10+ được khuyến nghị.

```bash
pip install -r requirements.txt
```

## 2. Chạy

```bash
streamlit run app.py
```

## 3. Những phần đã dựng

### Sinh viên
- Trang chủ theo giao diện tham chiếu
- Đặt món
- Tìm kiếm / lọc món
- Chi tiết món + số lượng + ghi chú
- Bách hóa thông minh
- Giỏ hàng
- Voucher
- 3 phương thức thanh toán mô phỏng
- Chọn địa điểm nhận hàng
- Đặt trước theo giờ
- QR đơn hàng / QR nhận món
- Theo dõi 4 trạng thái đơn
- Lịch sử đơn
- Đánh giá 5 sao
- Góp ý ẩn danh
- Tích điểm Loyalty
- Voucher đổi bằng điểm
- Thông báo
- Cá nhân hóa / gợi ý món

### Quản lý
- Dashboard đơn hàng
- Chuyển trạng thái đơn
- Theo dõi doanh thu demo
- Theo dõi tồn kho
- Mô phỏng quy trình vận hành 4 bước

## 4. Lưu ý

Đây là prototype phục vụ demo / portfolio. Dữ liệu nằm trong session của Streamlit, chưa có:
- database thật
- đăng nhập UTH thật
- cổng thanh toán thật
- API UTH
- hệ thống POS / bếp thật
- gửi thông báo thật

Các chức năng trên có thể được phát triển tiếp nếu muốn biến prototype thành MVP.

## Bản sửa tương tác

Bản này đã thay các ô chỉ mang tính minh họa bằng nút Streamlit thật ở các vị trí chính:
- Hero / Đặt món ngay
- 4 ô chức năng nhanh
- 4 danh mục dịch vụ
- Đặt trước theo giờ
- Điểm / voucher
- Bottom navigation
- Các nút thêm món, chi tiết, checkout, trạng thái, đánh giá, quản trị

Một số hình ảnh/card vẫn là phần trình bày nhưng luôn có nút hành động tương ứng ngay bên dưới.
