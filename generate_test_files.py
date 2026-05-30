import os
from PIL import Image

os.makedirs("test_cases", exist_ok=True)

# TC-01: Ảnh hợp lệ (Dung lượng nhỏ)
img = Image.new('RGB', (100, 100), color='blue')
img.save('test_cases/TC01_anh_hop_le.jpg')

# TC-02: Ngụy trang (Chứa text mã độc nhưng đuôi .jpg)
with open('test_cases/TC02_shell_gia_mao.jpg', 'w') as f:
    f.write('<?php echo "HACKED!"; system($_GET["cmd"]); ?>')

# TC-03: Quá lớn (File 3MB chứa byte rỗng để giả lập tràn ổ đĩa)
with open('test_cases/TC03_file_qua_lon.jpg', 'wb') as f:
    f.write(b'\0' * (3 * 1024 * 1024)) 

# TC-04 (MỚI): Sai định dạng rõ ràng (Upload file .txt, .exe, .sh)
with open('test_cases/TC04_ma_doc_trojan.exe', 'w') as f:
    f.write('MZ... (Gia lap file thuc thi)')

# TC-05 (MỚI): File đa đuôi (Double Extension) - Kỹ thuật Hacker hay dùng lừa bộ lọc
with open('test_cases/TC05_shell.php.jpg', 'w') as f:
    f.write('<?php system($_GET["cmd"]); ?>')

# TC-06 (MỚI): File không có đuôi mở rộng
with open('test_cases/TC06_file_vo_danh', 'w') as f:
    f.write('File rác không xác định định dạng')

print("✅ Đã tạo thành công 6 file Test Case đa dạng trong thư mục 'test_cases'.")