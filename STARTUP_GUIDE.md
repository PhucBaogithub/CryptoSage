# CryptoSage - Hướng Dẫn Khởi Chạy Toàn Diện

## 📋 Mục Lục
1. [Khởi Chạy Nhanh](#khởi-chạy-nhanh)
2. [Các Phương Pháp Khởi Chạy](#các-phương-pháp-khởi-chạy)
3. [Xoá File Không Cần Thiết](#xoá-file-không-cần-thiết)
4. [Kiểm Tra Trạng Thái](#kiểm-tra-trạng-thái)
5. [Khắc Phục Sự Cố](#khắc-phục-sự-cố)

---

## 🚀 Khởi Chạy Nhanh (30 Giây)

### Lần Đầu Tiên
```bash
# macOS/Linux
python3 start.py

# Windows
python start.py
```

**Kết quả mong đợi**:
```
╔════════════════════════════════════════════════════════════╗
║         CryptoSage - Bitcoin Futures Trading System        ║
╚════════════════════════════════════════════════════════════╝

✓ Python version: 3.9.x
✓ Virtual environment created
✓ Dependencies installed
✓ Ports cleared
✓ Backend started (PID: 12345)
✓ Frontend started (PID: 12346)

╔════════════════════════════════════════════════════════════╗
║                  ✓ All Servers Running!                    ║
╚════════════════════════════════════════════════════════════╝

📊 Dashboard URL:     http://localhost:3000
📚 API Docs:          http://localhost:8000/docs
🏥 Health Check:      http://localhost:8000/health
```

### Lần Tiếp Theo
```bash
python3 start.py
```

---

## 🎯 Các Phương Pháp Khởi Chạy

### Phương Pháp 1: Python Script (Khuyến Nghị) ⭐

**Ưu điểm**:
- ✅ Hoạt động trên tất cả hệ điều hành
- ✅ Tự động tạo virtual environment
- ✅ Tự động cài đặt dependencies
- ✅ Tự động dọn dẹp port
- ✅ Hiển thị thông tin chi tiết

**Cách sử dụng**:
```bash
# macOS/Linux
python3 start.py

# Windows
python start.py
```

---

### Phương Pháp 2: Shell Script (macOS/Linux)

**Ưu điểm**:
- ✅ Nhanh và nhẹ
- ✅ Hiển thị thông tin chi tiết
- ✅ Tự động dọn dẹp port

**Cách sử dụng**:
```bash
chmod +x start.sh
./start.sh
```

---

### Phương Pháp 3: Batch Script (Windows)

**Ưu điểm**:
- ✅ Giao diện Windows native
- ✅ Tự động mở cửa sổ riêng cho mỗi server

**Cách sử dụng**:
```bash
start.bat
```

---

### Phương Pháp 4: Chạy Thủ Công

**Khi nào sử dụng**: Nếu script không hoạt động

**Bước 1: Tạo Virtual Environment**
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**Bước 2: Cài Đặt Dependencies**
```bash
pip install -r requirements.txt
```

**Bước 3: Chạy Backend (Terminal 1)**
```bash
python3 -m src.api.server
```

**Bước 4: Chạy Frontend (Terminal 2)**
```bash
python3 frontend/server.py
```

---

## 🧹 Xoá File Không Cần Thiết

### Tự Động (Khuyến Nghị)
```bash
# Xoá tất cả file cache, log, temp
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.log" -delete 2>/dev/null
find . -type f -name ".DS_Store" -delete 2>/dev/null

echo "✓ Cleanup complete"
```

### Thủ Công
```bash
# Xoá __pycache__
rm -rf src/__pycache__
rm -rf frontend/__pycache__
rm -rf tests/__pycache__

# Xoá log files
rm -f logs/*.log

# Xoá .DS_Store (macOS)
find . -name ".DS_Store" -delete

# Xoá pytest cache
rm -rf .pytest_cache
```

### Các File Có Thể Xoá
- `logs/*.log` - Log files
- `__pycache__/` - Python cache
- `.pytest_cache/` - Test cache
- `*.pyc` - Compiled Python
- `.DS_Store` - macOS system file
- `*.egg-info/` - Package info

### Các File KHÔNG Nên Xoá
- ❌ `venv/` - Virtual environment
- ❌ `src/` - Source code
- ❌ `frontend/` - Frontend code
- ❌ `data/` - Data files
- ❌ `config/` - Configuration
- ❌ `.git/` - Git repository

---

## ✅ Kiểm Tra Trạng Thái

### Kiểm Tra Backend
```bash
curl http://localhost:8000/health
```

**Kết quả mong đợi**:
```json
{
    "status": "ok",
    "timestamp": "2025-10-20T11:00:00"
}
```

### Kiểm Tra Frontend
```bash
curl http://localhost:3000
```

**Kết quả mong đợi**: HTML dashboard

### Kiểm Tra API
```bash
curl "http://localhost:8000/api/prices/current?symbols=BTCUSDT"
```

**Kết quả mong đợi**:
```json
{
    "BTCUSDT": {
        "price": "110710.5",
        "timestamp": "2025-10-20T11:00:00"
    }
}
```

### Kiểm Tra Port
```bash
# macOS/Linux
lsof -i :8000
lsof -i :3000

# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :3000
```

---

## 🔧 Khắc Phục Sự Cố

### Lỗi: "Port already in use"
```bash
# Tìm process
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Dừng process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Lỗi: "ModuleNotFoundError"
```bash
# Cài đặt lại dependencies
pip install -r requirements.txt --upgrade
```

### Lỗi: "Permission denied"
```bash
# Cấp quyền thực thi
chmod +x start.sh
chmod +x start.py
```

### Lỗi: "Python not found"
```bash
# Kiểm tra phiên bản
python3 --version

# Cài đặt Python 3.9+
# macOS: brew install python3
# Linux: sudo apt-get install python3
# Windows: https://python.org
```

### Lỗi: "Connection refused"
```bash
# Kiểm tra xem server có chạy không
curl http://localhost:8000/health
curl http://localhost:3000

# Nếu không, khởi chạy lại
python3 start.py
```

---

## 📊 Các Lệnh Hữu Ích

```bash
# Khởi chạy
python3 start.py                    # Python script
./start.sh                          # Shell script
start.bat                           # Batch script

# Backend riêng
python3 -m src.api.server

# Frontend riêng
python3 frontend/server.py

# Cài đặt dependencies
pip install -r requirements.txt

# Kiểm tra phiên bản
python3 --version
pip --version

# Xoá cache
find . -type d -name "__pycache__" -exec rm -rf {} +

# Xoá log
rm -f logs/*.log

# Kiểm tra port
lsof -i :8000
lsof -i :3000

# Dừng process
kill -9 <PID>
```

---

## 🌐 Truy Cập Ứng Dụng

| Dịch Vụ | URL | Mô Tả |
|---------|-----|-------|
| Dashboard | http://localhost:3000 | Giao diện chính |
| API Docs | http://localhost:8000/docs | Tài liệu API |
| Health | http://localhost:8000/health | Kiểm tra trạng thái |
| API | http://localhost:8000/api | Endpoint API |

---

## 💡 Mẹo Hữu Ích

1. **Lần đầu tiên**: Sử dụng `python3 start.py` để tự động setup
2. **Lần tiếp theo**: Chỉ cần chạy `python3 start.py` lại
3. **Dừng**: Nhấn `Ctrl+C` để dừng tất cả server
4. **Debug**: Kiểm tra console (F12) trong browser
5. **Logs**: Xem logs trong terminal hoặc `logs/` folder

---

## 🔐 Bảo Mật

⚠️ **QUAN TRỌNG**:
- ❌ KHÔNG sử dụng Live Trading mode với tiền thật
- ✅ Luôn sử dụng Paper Trading mode để học tập
- ✅ Kiểm tra kỹ chiến lược trước khi giao dịch thực

---

## 📞 Hỗ Trợ

- **GitHub**: https://github.com/PhucBaogithub/CryptoSage
- **Issues**: https://github.com/PhucBaogithub/CryptoSage/issues
- **Docs**: Xem SETUP.md và QUICK_START.md

---

**Phiên Bản**: 1.0.0  
**Cập Nhật**: 2025-10-20  
**Trạng Thái**: ✅ Production Ready

