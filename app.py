import os, uuid
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import threading
import webbrowser

app = Flask(__name__)
app.secret_key = "cyber_fortress_cf10_fptu"

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
        img.verify() 
        file_stream.seek(0)
        return True
    except Exception:
        return False

def get_file_size(file_stream):
    file_stream.seek(0, os.SEEK_END)
    size = file_stream.tell()
    file_stream.seek(0)
    return size

@app.route('/')
def index():
    return render_template('index.html')

# ==========================================
# 🚨 LUỒNG 1: VULNERABLE (Bản lỗi)
# ==========================================
@app.route('/upload_vuln', methods=['POST'])
def upload_vuln():
    if 'file' not in request.files:
        return jsonify({"title": "Lỗi", "msg": "Không tìm thấy file"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"title": "Lỗi", "msg": "Chưa chọn file"}), 400
    
    file_size = get_file_size(file)
    filename = file.filename
    filepath = os.path.join(UPLOAD_VULN, filename)
    file.save(filepath)
    
    return jsonify({
        "status": "danger",
        "title": "❌ CẢNH BÁO: MÁY CHỦ BỊ XÂM NHẬP!",
        "msg": "Hệ thống Lỗi đã tiếp nhận file thành công (Rất nguy hiểm).",
        "reasons": [
            "Lỗi hệ thống: Không có lớp kiểm tra giới hạn dung lượng.",
            "Lỗi hệ thống: Không có danh sách Whitelist để lọc đuôi file.",
            "Lỗi hệ thống: Bỏ qua bước kiểm tra chữ ký/cấu trúc Byte (Header) của file."
        ],
        "file_info": {
            "name": filename,
            "mime_type": file.mimetype,
            "size": f"{file_size / 1024:.2f} KB",
            "saved_as": filepath
        }
    }), 200

# ==========================================
# 🛡️ LUỒNG 2: SECURE (Bản vá lỗi)
# ==========================================
@app.route('/upload_secure', methods=['POST'])
def upload_secure():
    if 'file' not in request.files:
        return jsonify({"title": "Lỗi", "msg": "Không tìm thấy file"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"title": "Lỗi", "msg": "Chưa chọn file"}), 400

    filename = file.filename
    file_size = get_file_size(file)
    
    file_data = {
        "name": filename,
        "mime_type": file.mimetype,
        "size": f"{file_size / 1024:.2f} KB"
    }

    # BỘ QUÉT TÍCH LŨY ĐA LỖI
    errors_found = []

    # Kiểm tra 1: Dung lượng
    if file_size > MAX_FILE_SIZE:
        errors_found.append(f"Vượt quá dung lượng an toàn (Kích thước: {file_size / (1024*1024):.2f} MB > 2.0 MB).")

    # Kiểm tra 2: Đuôi file
    if not allowed_file(filename):
        errors_found.append("Sai định dạng đuôi file (Whitelist chỉ cấp phép: .jpg, .jpeg, .png).")

    # Kiểm tra 3: Magic Bytes (Nội dung bên trong)
    if not is_real_image(file):
        errors_found.append("Cảnh báo giả mạo Header! Cấu trúc byte bên trong không phải là ảnh hợp lệ.")

    # NẾU PHÁT HIỆN LỖI (Dù chỉ 1 lỗi) -> CHẶN NGAY
    if errors_found:
        return jsonify({
            "status": "blocked",
            "title": "🛡️ BỊ CHẶN: PHÁT HIỆN FILE KHÔNG HỢP LỆ!",
            "msg": "Hệ thống từ chối lưu file này do vi phạm chính sách bảo mật.",
            "reasons": errors_found,
            "file_info": file_data
        }), 403

    # NẾU FILE AN TOÀN (Vượt qua 3 lớp trên) -> MÃ HÓA TÊN FILE VÀ LƯU
    ext = filename.rsplit('.', 1)[1].lower()
    safe_filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_SECURE, safe_filename)
    file.save(filepath)
    
    file_data["saved_as"] = safe_filename

    return jsonify({
        "status": "success",
        "title": "✅ TẢI LÊN AN TOÀN!",
        "msg": "File hợp lệ đã được lưu trữ thành công.",
        "reasons": ["Vượt qua toàn bộ 3 lớp kiểm tra bảo mật (Dung lượng, Whitelist, Magic Bytes)."],
        "file_info": file_data
    }), 200

def open_browser():
    webbrowser.open_new("http://localhost:5000/")

if __name__ == '__main__':
    threading.Timer(1.5, open_browser).start()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)