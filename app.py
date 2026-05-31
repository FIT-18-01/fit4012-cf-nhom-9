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

# ==========================================
# 🛠️ HÀM MỚI: TỰ ĐỘNG ĐỊNH DẠNG DUNG LƯỢNG
# ==========================================
def format_size(size_in_bytes):
    if size_in_bytes >= 1024 * 1024:
        return f"{size_in_bytes / (1024 * 1024):.2f} MB"
    elif size_in_bytes >= 1024:
        return f"{size_in_bytes / 1024:.2f} KB"
    else:
        return f"{size_in_bytes} Bytes"

@app.route('/')
def index():
    return render_template('index.html')

# ==========================================
# 🚨 LUỒNG 1: VULNERABLE (HỆ THỐNG LỖI)
# ==========================================
@app.route('/upload_vuln', methods=['POST'])
def upload_vuln():
    files = request.files.getlist('file')
    if not files or files[0].filename == '':
        return jsonify({"error": "Chưa chọn file nào!"}), 400
    
    results = []
    for file in files:
        if file.filename == '': continue
        
        filename = file.filename
        file_size = get_file_size(file)
        filepath = os.path.join(UPLOAD_VULN, filename)
        file.save(filepath)
        
        trace_log = [
            f"⚠️ Bước 1: Tiếp nhận file '{filename}'.",
            f"🚨 Bước 2: LƯU TRỰC TIẾP vào hệ thống với tên gốc."
        ]
        
        results.append({
            "status": "danger",
            "title": "❌ CẢNH BÁO: MÁY CHỦ BỊ XÂM NHẬP!",
            "logs": trace_log,
            "file_info": {
                "name": filename,
                "mime_type": file.mimetype,
                "size": format_size(file_size), # Dùng hàm định dạng mới
                "saved_as": filepath
            }
        })
        
    return jsonify({"results": results}), 200

# ==========================================
# 🛡️ LUỒNG 2: SECURE (HỆ THỐNG VÁ LỖI)
# ==========================================
@app.route('/upload_secure', methods=['POST'])
def upload_secure():
    files = request.files.getlist('file')
    if not files or files[0].filename == '':
        return jsonify({"error": "Chưa chọn file nào!"}), 400

    results = []
    for file in files:
        if file.filename == '': continue

        filename = file.filename
        file_size = get_file_size(file)
        mime_type = file.mimetype
        trace_log = []
        is_safe = True

        trace_log.append(f"ℹ️ Bước 1: Tiếp nhận gói tin '{filename}'.")

        if file_size > MAX_FILE_SIZE:
            trace_log.append("❌ Bước 2: KIỂM TRA DUNG LƯỢNG -> [THẤT BẠI] Vượt quá 2MB.")
            is_safe = False
        else:
            trace_log.append("✅ Bước 2: KIỂM TRA DUNG LƯỢNG -> [HỢP LỆ].")

        if not allowed_file(filename):
            trace_log.append("❌ Bước 3: KIỂM TRA ĐỊNH DẠNG -> [THẤT BẠI] Đuôi file bị cấm.")
            is_safe = False
        else:
            trace_log.append("✅ Bước 3: KIỂM TRA ĐỊNH DẠNG -> [HỢP LỆ].")

        if is_safe:
            if not is_real_image(file):
                trace_log.append("❌ Bước 4: QUÉT MAGIC BYTES -> [THẤT BẠI] Giả mạo Header.")
                is_safe = False
            else:
                trace_log.append("✅ Bước 4: QUÉT MAGIC BYTES -> [HỢP LỆ] Cấu trúc chuẩn.")
        else:
            trace_log.append("⚠️ Bước 4: QUÉT MAGIC BYTES -> Bỏ qua do đã lỗi từ trước.")

        if is_safe:
            ext = filename.rsplit('.', 1)[1].lower()
            safe_filename = f"{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(UPLOAD_SECURE, safe_filename)
            file.save(filepath)
            
            trace_log.append(f"✅ Bước 5: KHỬ ĐỘC TÊN FILE -> Đã lưu an toàn.")
            
            results.append({
                "status": "success",
                "title": "✅ TẢI LÊN THÀNH CÔNG & AN TOÀN",
                "logs": trace_log,
                "file_info": {
                    "name": filename,
                    "mime_type": mime_type,
                    "size": format_size(file_size), # Dùng hàm định dạng mới
                    "saved_as": safe_filename
                }
            })
        else:
            trace_log.append("🛡️ Bước 5: HỦY GÓI TIN -> Chặn đứng nỗ lực tấn công.")
            results.append({
                "status": "blocked",
                "title": "🛡️ ĐÃ CHẶN ĐỨNG FILE ĐỘC HẠI",
                "logs": trace_log,
                "file_info": {
                    "name": filename,
                    "mime_type": mime_type,
                    "size": format_size(file_size) # Dùng hàm định dạng mới
                }
            })

    return jsonify({"results": results}), 200

def open_browser():
    webbrowser.open_new("http://localhost:5000/")

if __name__ == '__main__':
    threading.Timer(1.5, open_browser).start()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)