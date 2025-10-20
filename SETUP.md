# CryptoSage - Hướng Dẫn Cài Đặt và Sử Dụng

## 📋 Mục Lục
1. [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
2. [Cài Đặt](#cài-đặt)
3. [Cấu Hình](#cấu-hình)
4. [Chạy Ứng Dụng](#chạy-ứng-dụng)
5. [Truy Cập Dashboard](#truy-cập-dashboard)
6. [Các Tính Năng](#các-tính-năng)
7. [Khắc Phục Sự Cố](#khắc-phục-sự-cố)

---

## 🖥️ Yêu Cầu Hệ Thống

### Phần Cứng
- **CPU**: Intel/AMD 2GHz hoặc cao hơn
- **RAM**: Tối thiểu 4GB (khuyến nghị 8GB)
- **Ổ Cứng**: Tối thiểu 2GB dung lượng trống
- **Kết Nối**: Internet ổn định

### Phần Mềm
- **Hệ Điều Hành**: Windows 10+, macOS 10.14+, hoặc Linux (Ubuntu 18.04+)
- **Python**: Phiên bản 3.9 hoặc cao hơn
- **Git**: Để clone repository (tùy chọn)

### Kiểm Tra Phiên Bản Python
```bash
python3 --version
# Kết quả mong đợi: Python 3.9.x hoặc cao hơn
```

---

## 📦 Cài Đặt

### Bước 1: Clone Repository
```bash
# Nếu có Git
git clone https://github.com/PhucBaogithub/CryptoSage.git
cd CryptoSage

# Hoặc tải file ZIP từ GitHub và giải nén
```

### Bước 2: Tạo Virtual Environment (Khuyến Nghị)
```bash
# Trên Windows
python -m venv venv
venv\Scripts\activate

# Trên macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài Đặt Dependencies

#### Backend Dependencies
```bash
# Cài đặt các thư viện Python cần thiết
pip install -r requirements.txt

# Hoặc cài đặt thủ công
pip install fastapi uvicorn aiohttp pydantic torch numpy pandas scikit-learn
```

#### Frontend Dependencies
Frontend sử dụng vanilla JavaScript, không cần cài đặt thêm.

---

## ⚙️ Cấu Hình

### Cấu Hình Backend
Tệp cấu hình chính: `src/config.py` (nếu có)

**Các biến môi trường (tùy chọn)**:
```bash
# Cổng API Backend (mặc định: 8000)
export API_PORT=8000

# Cổng Frontend (mặc định: 3000)
export FRONTEND_PORT=3000

# Chế độ Debug (mặc định: False)
export DEBUG=False
```

### Cấu Hình Frontend
Tệp cấu hình: `frontend/js/app.js`

**API Base URL** (dòng ~50):
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

---

## 🚀 Chạy Ứng Dụng

### Phương Pháp 1: Chạy Riêng Lẻ (Khuyến Nghị cho Phát Triển)

#### Terminal 1 - Chạy Backend
```bash
cd /đường/dẫn/đến/CryptoSage
source venv/bin/activate  # Hoặc venv\Scripts\activate trên Windows
python3 -m src.api.server
```

Kết quả mong đợi:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

#### Terminal 2 - Chạy Frontend
```bash
cd /đường/dẫn/đến/CryptoSage
python3 frontend/server.py
```

Kết quả mong đợi:
```
Server running on http://localhost:3000
```

### Phương Pháp 2: Chạy Cùng Lúc (Tự Động)
```bash
# Chỉ trên macOS/Linux
python3 run_all.py
```

---

## 🌐 Truy Cập Dashboard

### URL Chính
```
http://localhost:3000
```

### Các Endpoint API Chính
- **Health Check**: `http://localhost:8000/health`
- **API Docs**: `http://localhost:8000/docs`
- **Prices**: `http://localhost:8000/api/prices/current?symbols=BTCUSDT,ETHUSDT`

---

## 📊 Các Tính Năng

### 1. **Overview Tab** 📈
- Hiển thị giá tiền điện tử theo thời gian thực
- Biểu đồ giá 24 giờ
- Thông tin thị trường tổng quát

### 2. **Predictions Tab** 🔮
- Dự đoán giá dài hạn (3-36 tháng)
- Dự đoán giá ngắn hạn (1-72 giờ)
- Tín hiệu giao dịch (Buy/Sell/Hold)
- Độ tin cậy của dự đoán

### 3. **Data Tab** 📥
- Thu thập dữ liệu lịch sử
- Hỗ trợ nhiều timeframe
- Lưu trữ dữ liệu cục bộ

### 4. **Models Tab** 🤖
- Huấn luyện mô hình ML
- Xem trạng thái mô hình
- Cải thiện độ chính xác

### 5. **Backtest Tab** 🧪
- Kiểm tra chiến lược giao dịch
- Xem kết quả lịch sử
- Phân tích hiệu suất

### 6. **Futures Trading Tab** 💹
- Giao dịch tương lai
- Quản lý vị trí
- Tính toán P&L theo thời gian thực

### 7. **Paper Trading Tab** 📝
- Giao dịch giả lập
- Không sử dụng tiền thật
- Học tập an toàn

### 8. **Risk Tab** ⚠️
- Tính toán rủi ro
- Quản lý vị trí
- Tính giá thanh lý

---

## 🔧 Khắc Phục Sự Cố

### Lỗi: "Connection refused" khi truy cập localhost:3000
**Giải pháp**:
```bash
# Kiểm tra xem frontend server có chạy không
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Nếu không chạy, khởi động lại
python3 frontend/server.py
```

### Lỗi: "Connection refused" khi truy cập localhost:8000
**Giải pháp**:
```bash
# Kiểm tra xem backend server có chạy không
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Nếu không chạy, khởi động lại
python3 -m src.api.server
```

### Lỗi: "ModuleNotFoundError: No module named 'fastapi'"
**Giải pháp**:
```bash
# Cài đặt lại dependencies
pip install -r requirements.txt

# Hoặc cài đặt thủ công
pip install fastapi uvicorn aiohttp
```

### Lỗi: "Port already in use"
**Giải pháp**:
```bash
# Tìm process sử dụng port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Dừng process (thay PID bằng số thực tế)
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Lỗi: "Giá tiền điện tử không cập nhật"
**Giải pháp**:
- Kiểm tra kết nối Internet
- Kiểm tra xem Binance API có hoạt động không
- Thử làm mới trang (F5)

### Lỗi: "Nút Place Order không hoạt động"
**Giải pháp**:
- Kiểm tra xem backend server có chạy không
- Kiểm tra console (F12) để xem lỗi chi tiết
- Kiểm tra xem tất cả trường form đã được điền không

---

## 📝 Ghi Chú Quan Trọng

### Bảo Mật
- ⚠️ **KHÔNG** sử dụng Live Trading mode với tiền thật
- Luôn sử dụng Paper Trading mode để học tập
- Kiểm tra kỹ chiến lược trước khi giao dịch thực

### Hiệu Suất
- Ứng dụng cập nhật giá mỗi 30 giây
- Dự đoán được cập nhật mỗi 5 phút
- Sử dụng Binance Public API (không cần API key)

### Hỗ Trợ
- Kiểm tra GitHub Issues: https://github.com/PhucBaogithub/CryptoSage/issues
- Xem tài liệu API: http://localhost:8000/docs

---

## 📞 Liên Hệ & Hỗ Trợ

**GitHub Repository**: https://github.com/PhucBaogithub/CryptoSage

**Các Tính Năng Sắp Tới**:
- WebSocket cho cập nhật giá real-time
- Biểu đồ nâng cao với TradingView
- Cảnh báo giá tự động
- Xuất dữ liệu CSV/Excel

---

**Phiên Bản**: 1.0.0  
**Cập Nhật Lần Cuối**: 2025-10-20  
**Trạng Thái**: Production Ready ✅

