# Threat Model - Cyber Fortress
## 1. Asset - Tài sản cần bảo vệ
- Không gian lưu trữ của máy chủ (Disk space).
- Dữ liệu cá nhân của người dùng và file hệ thống.
- Tính toàn vẹn của mã nguồn trang web.
- Tính sẵn sàng của dịch vụ (Service Availability).

## 2. Threat - Mối đe dọa
- Người dùng độc hại cố tình tải lên file sai quy định.
- Kẻ tấn công bên ngoài (Hacker/Script Kiddie) muốn chiếm quyền Server.
- Bot/script tự động rà quét và upload shell hàng loạt.

## 3. Vulnerability - Lỗ hổng
- **Unrestricted File Upload (CF10):** Hệ thống cho phép người dùng upload file nhưng thiếu cơ chế kiểm tra (Validation) đối với định dạng (Extension), kích thước (Size) và chữ ký nội dung (Magic Bytes). Đồng thời, hệ thống lưu file bằng tên gốc của người dùng vào thư mục có quyền thực thi.

## 4. Impact - Tác động
- **Mất tính sẵn sàng (DoS):** Gây tràn bộ nhớ ổ đĩa do upload file kích thước siêu lớn.
- **Mất toàn vẹn dữ liệu:** Tấn công Path Traversal ghi đè file cấu hình hệ thống.
- **Chiếm quyền tài khoản / Server (RCE):** Thực thi mã độc (Webshell) để kiểm soát máy chủ từ xa, dẫn đến mất bí mật dữ liệu.
- **Defacement:** Thay đổi giao diện website bằng hình ảnh độc hại.

## 5. Mitigation - Biện pháp giảm thiểu
- **Biện pháp kỹ thuật:** 1. Dùng Whitelist thay vì Blacklist (chỉ cho phép .jpg, .png).
  2. Giới hạn dung lượng tối đa (Max File Size = 2MB).
  3. Kiểm tra Header/MIME type thực tế của file bằng thư viện xử lý ảnh chuyên dụng (Pillow).
  4. Lưu file ở thư mục không có quyền thực thi (no-exec).
  5. Đổi tên file ngẫu nhiên (Mã hóa UUID) trước khi lưu.
- **Biện pháp quy trình:** Cập nhật bản vá thư viện xử lý file thường xuyên.
- **Biện pháp nâng cao nhận thức:** Đào tạo lập trình viên nguyên tắc "Không bao giờ tin tưởng Input của người dùng".