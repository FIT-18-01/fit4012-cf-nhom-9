[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/JLI_HvmF)


# Báo cáo Thực hành Cyber Fortress - Đề tài CF10

<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<br>
<h2 align="center">
    CRYPTOGRAPHY AND CYBER SECURITY
</h2>
<br>
<div align="center">
    <p align="center">
        <img src="fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

**Giảng Viên - ThS. Lê Thị Thùy Trang**

**Học phần:** FIT4012 - Nhập môn An toàn bảo mật thông tin
**Chủ đề:** File Upload Vulnerability

## 1. Hướng dẫn cài đặt và chạy Demo
- **Bước 1:** Cài đặt Python 3.x.
- **Bước 2:** Mở Terminal tại thư mục dự án và cài đặt thư viện:
  `pip install -r requirements.txt`
- **Bước 3:** Chạy kịch bản tạo file test (tự động sinh ra 3 file trong thư mục `test_cases`):
  `python generate_test_files.py` (File đã tạo)
- **Bước 4:** Khởi chạy máy chủ web cục bộ:
  `python app.py`
- **Bước 5:** Trình duyệt sẽ tự động mở giao diện tại `http://localhost:5000` (hoặc truy cập thủ công).

## 2. Các Test Case đã thực hiện
Hệ thống được chia làm 2 luồng xử lý độc lập để so sánh: Luồng Vulnerable (bỏ qua kiểm tra) và Luồng Secure (áp dụng Defense in Depth).

| Mã Test | Mô tả Input | Kết quả bên Vulnerable | Kết quả bên Secure | Đánh giá |
| :-- | :-- | :-- | :-- | :-- |
| **TC-01** | Upload file `TC01_anh_hop_le.jpg` | Thành công, lưu nguyên tên gốc | Thành công, file bị đổi tên ngẫu nhiên (UUID) | PASS |
| **TC-02** | Upload file `TC02_shell_gia_mao.jpg` | Bị qua mặt, nhận file chứa mã độc | Phát hiện Header không phải là ảnh, chặn upload | PASS |
| **TC-03** | Upload file `TC03_file_qua_lon.jpg` | Bị qua mặt, nhận file 3MB | Giới hạn 2MB kích hoạt, chặn upload | PASS |
| **TC-04** | **Upload file sai định dạng gốc** (`TC04_ma_doc_trojan.exe`) | **Nguy hiểm:** Upload thành công. Hệ thống bị tiêm nhiễm mã độc. | **An toàn:** Bị chặn lại ở lớp kiểm tra thứ 2 do đuôi `.exe` không nằm trong danh sách cho phép (Whitelist). | PASS |
| **TC-05** | **Upload file đa đuôi lừa đảo** (`TC05_shell.php.jpg`) | **Nguy hiểm:** Upload thành công. | **An toàn:** Kẻ gian lách được qua lớp Whitelist nhưng bị chặn lại ở lớp thứ 3 (Kiểm tra Header ảnh bằng Pillow). Thể hiện phòng thủ đa lớp hoạt động hoàn hảo. | PASS |
| **TC-06** | **Upload file không có đuôi** (`TC06_file_vo_danh`) | **Nguy hiểm:** Upload thành công. | **An toàn:** Bị từ chối vì hệ thống bắt buộc file phải tuân thủ chuẩn định dạng có đuôi mở rộng. | PASS |

*Lưu ý an toàn: Tất cả test case chỉ được thực hiện trên localhost, các file mã độc được giả lập bằng text tĩnh, không có khả năng thực thi thực tế, tuân thủ đúng cam kết đạo đức môn học.*
