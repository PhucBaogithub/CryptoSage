# CryptoSage - Hướng Dẫn Khởi Chạy Nhanh

## 🚀 Khởi Chạy Dễ Dàng

### Phương Pháp 1: Sử Dụng Script Python (Khuyến Nghị - Cross-Platform)

#### macOS/Linux
```bash
# Cấp quyền thực thi
chmod +x start.py

# Chạy script
python3 start.py
```

#### Windows
```bash
# Chạy script
python start.py
```

**Ưu điểm**:
- ✅ Hoạt động trên tất cả hệ điều hành
- ✅ Tự động tạo virtual environment
- ✅ Tự động cài đặt dependencies
- ✅ Tự động dọn dẹp port
- ✅ Hiển thị thông tin chi tiết

---

### Phương Pháp 2: Sử Dụng Shell Script (macOS/Linux)

```bash
# Cấp quyền thực thi
chmod +x start.sh

# Chạy script
./start.sh
```

**Ưu điểm**:
- ✅ Nhanh và nhẹ
- ✅ Hiển thị thông tin chi tiết
- ✅ Tự động dọn dẹp port

---

### Phương Pháp 3: Sử Dụng Batch Script (Windows)

```bash
# Chạy script
start.bat
```

**Ưu điểm**:
- ✅ Giao diện Windows native
- ✅ Tự động mở cửa sổ riêng cho mỗi server

---

### Phương Pháp 4: Chạy Thủ Công (Nếu Script Không Hoạt Động)

#### Bước 1: Tạo Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### Bước 2: Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

#### Bước 3: Chạy Backend (Terminal 1)
```bash
python3 -m src.api.server
```

#### Bước 4: Chạy Frontend (Terminal 2)
```bash
python3 frontend/server.py
```

---

## 📍 Truy Cập Ứng Dụng

Sau khi khởi chạy, bạn có thể truy cập:

| Dịch Vụ | URL | Mô Tả |
|---------|-----|-------|
| **Dashboard** | http://localhost:3000 | Giao diện chính |
| **API Docs** | http://localhost:8000/docs | Tài liệu API (Swagger) |
| **Health Check** | http://localhost:8000/health | Kiểm tra trạng thái |
| **API Base** | http://localhost:8000/api | Endpoint API |

---

## 🛑 Dừng Ứng Dụng

### Nếu Sử Dụng Script
- Nhấn **Ctrl+C** trong terminal

### Nếu Chạy Thủ Công
- Nhấn **Ctrl+C** trong mỗi terminal

### Nếu Sử Dụng Batch Script (Windows)
- Đóng cửa sổ batch script
- Đóng cửa sổ Backend
- Đóng cửa sổ Frontend

---

## 🔧 Khắc Phục Sự Cố

### Lỗi: "Port already in use"
```bash
# macOS/Linux - Tìm process sử dụng port
lsof -i :8000
lsof -i :3000

# Dừng process (thay PID bằng số thực tế)
kill -9 <PID>

# Windows - Tìm process sử dụng port
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Dừng process
taskkill /PID <PID> /F
```

### Lỗi: "ModuleNotFoundError"
```bash
# Cài đặt lại dependencies
pip install -r requirements.txt
```

### Lỗi: "Permission denied" (macOS/Linux)
```bash
# Cấp quyền thực thi cho script
chmod +x start.sh
chmod +x start.py
```

### Lỗi: "Python not found"
```bash
# Kiểm tra phiên bản Python
python3 --version

# Nếu không có, cài đặt Python 3.9+
# macOS: brew install python3
# Linux: sudo apt-get install python3
# Windows: Tải từ python.org
```

---

## 📊 Các Tính Năng Chính

### 1. Overview Tab 📈
- Giá tiền điện tử theo thời gian thực
- Biểu đồ 24 giờ
- Thông tin thị trường

### 2. Predictions Tab 🔮
- Dự đoán giá dài hạn (3-36 tháng)
- Dự đoán giá ngắn hạn (1-72 giờ)
- Tín hiệu giao dịch

### 3. Futures Trading Tab 💹
- Giao dịch tương lai
- Quản lý vị trí
- P&L theo thời gian thực

### 4. Paper Trading Tab 📝
- Giao dịch giả lập
- Không sử dụng tiền thật
- Học tập an toàn

### 5. Risk Tab ⚠️
- Tính toán rủi ro
- Quản lý vị trí
- Giá thanh lý

---

## 💡 Mẹo Hữu Ích

### Cập Nhật Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Xem Logs
```bash
# Backend logs
tail -f logs/trading.log

# Frontend logs
# Kiểm tra console trong browser (F12)
```

### Kiểm Tra API
```bash
# Health check
curl http://localhost:8000/health

# Lấy giá Bitcoin
curl "http://localhost:8000/api/prices/current?symbols=BTCUSDT"

# Xem tất cả endpoints
curl http://localhost:8000/docs
```

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
- **Docs**: Xem SETUP.md để biết thêm chi tiết

---

## 🎯 Các Lệnh Hữu Ích

```bash
# Khởi chạy (Python)
python3 start.py

# Khởi chạy (Shell - macOS/Linux)
./start.sh

# Khởi chạy (Batch - Windows)
start.bat

# Khởi chạy Backend riêng
python3 -m src.api.server

# Khởi chạy Frontend riêng
python3 frontend/server.py

# Cài đặt dependencies
pip install -r requirements.txt

# Kiểm tra phiên bản Python
python3 --version

# Kiểm tra port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

---

**Phiên Bản**: 1.0.0  
**Cập Nhật**: 2025-10-20  
**Trạng Thái**: ✅ Production Ready

