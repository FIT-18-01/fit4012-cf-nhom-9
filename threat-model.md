# Mô hình Mối đe dọa (Threat Model) - File Upload

- **Tài sản cần bảo vệ:** Máy chủ lưu trữ file, thông tin người dùng, tính sẵn sàng của ổ đĩa.
- **Mối đe dọa / Lỗ hổng:** Giao diện Upload không validate đầu vào (Unrestricted File Upload).
- **Tác động (Impact):**
  - Thực thi mã từ xa (RCE): Kẻ tấn công up file shell (`.php`, `.exe`) và chiếm quyền server.
  - Tấn công từ chối dịch vụ (DoS): Kẻ tấn công up file dung lượng cực lớn làm tràn bộ nhớ ổ đĩa.
  - Tấn công Path Traversal: Gửi tên file dạng `../../../etc/passwd` để ghi đè file hệ thống quan trọng.
- **Biện pháp giảm thiểu (Mitigation):**
  1. Áp dụng Whitelist (chỉ cho phép .jpg, .png).
  2. Giới hạn Max File Size (ví dụ: 2MB).
  3. Validate MIME type và đọc byte header để chống file ngụy trang.
  4. Đổi tên file ngẫu nhiên (UUID) trước khi lưu.
  5. Lưu file ở thư mục không có quyền thực thi (no-exec).