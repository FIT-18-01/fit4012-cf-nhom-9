import os, uuid
from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
from PIL import Image
import threading
import webbrowser

app = Flask(__name__)
app.secret_key = "cyber_fortress_cf10"

# Cấu hình
UPLOAD_VULN = 'uploads/vulnerable/'
UPLOAD_SECURE = 'uploads/secure/'
os.makedirs(UPLOAD_VULN, exist_ok=True)
os.makedirs(UPLOAD_SECURE, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_real_image(file_stream):
    try:
        img = Image.open(file_stream)
        img.verify() # Kiểm tra byte header có thực sự là ảnh không
        file_stream.seek(0) # Reset stream lại từ đầu sau khi đọc
        return True
    except Exception:
        return False

@app.route('/')
def index():
    return render_template('index.html')


# ==========================================
# LUỒNG 1: VULNERABLE (Bản lỗi)
# Không kiểm tra size, không đổi tên file, không kiểm tra nội dung
# ==========================================
@app.route('/upload_vuln', methods=['POST'])
def upload_vuln():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    # RỦI RO: Lưu trực tiếp bằng tên gốc vào thư mục
    filename = file.filename
    filepath = os.path.join(UPLOAD_VULN, filename)
    file.save(filepath)
    
    return f"❌ [VULNERABLE] Upload thành công! File lưu tại: {filepath}"

# ==========================================
# LUỒNG 2: SECURE (Bản vá lỗi)
# White-list đuôi file, giới hạn Size, đổi tên UUID, kiểm tra nội dung
# ==========================================
@app.route('/upload_secure', methods=['POST'])
def upload_secure():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # 1. Kiểm tra kích thước file (Giới hạn 2MB)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if file_size > MAX_FILE_SIZE:
        return "✅ [SECURE] Bị chặn: Dung lượng file vượt quá 2MB!", 403

    # 2. Whitelist Extension
    if not allowed_file(file.filename):
        return "✅ [SECURE] Bị chặn: Đuôi file không được phép!", 403

    # 3. Kiểm tra MIME / Header thực tế (Phòng Hacker đổi đuôi .php thành .jpg)
    if not is_real_image(file):
        return "✅ [SECURE] Bị chặn: File bị làm giả mạo, nội dung không phải là ảnh!", 403

    # 4. Đổi tên file ngẫu nhiên (UUID) để tránh path traversal và ghi đè
    ext = file.filename.rsplit('.', 1)[1].lower()
    safe_filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_SECURE, safe_filename)
    
    file.save(filepath)
    return f"🛡️ [SECURE] Upload an toàn thành công! Đã đổi tên thành: {safe_filename}"

def open_browser():
    # Tự động mở link trên máy của bạn khi chạy code
    webbrowser.open_new("http://localhost:5000/")

if __name__ == '__main__':
    # Chạy trên 0.0.0.0 để các máy khác có thể truy cập qua IP của bạn
    HOST = '0.0.0.0'
    PORT = 5000
    
    # Hẹn 1.5 giây sau khi bật Server thì tự động gọi trình duyệt lên
    threading.Timer(1.5, open_browser).start()
    
    # use_reloader=False để tránh trình duyệt bị mở thành nhiều tab
    app.run(host=HOST, port=PORT, debug=True, use_reloader=False)