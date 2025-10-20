# CryptoSage - Tóm Tắt Dự Án

## 📊 Tổng Quan

**CryptoSage** là một hệ thống giao dịch Bitcoin tương lai (Futures Trading) với:
- 🎯 Dashboard tương tác với 8 tab chức năng
- 📈 Dự đoán giá sử dụng AI/ML
- 💹 Giao dịch tương lai với quản lý rủi ro
- 📝 Giao dịch giả lập (Paper Trading)
- 🔍 Phân tích dữ liệu và backtesting
- ⚠️ Quản lý rủi ro toàn diện

---

## 🚀 Khởi Chạy Nhanh

### Lần Đầu Tiên (30 giây)
```bash
python3 start.py
```

### Truy Cập
- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

---

## 📁 Cấu Trúc Dự Án

```
CryptoSage/
├── frontend/                 # Frontend (HTML/CSS/JS)
│   ├── index.html           # Dashboard chính
│   ├── js/app.js            # Logic ứng dụng
│   ├── css/                 # Stylesheet
│   └── server.py            # Frontend server (port 3000)
│
├── src/                      # Backend (Python)
│   ├── api/server.py        # FastAPI server (port 8000)
│   ├── models/              # ML models
│   ├── data/                # Data processing
│   ├── backtesting/         # Backtesting engine
│   ├── risk_management/     # Risk management
│   └── utils/               # Utilities
│
├── config/                   # Configuration files
├── data/                     # Data storage
├── logs/                     # Log files
├── tests/                    # Unit & integration tests
│
├── start.py                 # Startup script (Python)
├── start.sh                 # Startup script (Shell)
├── start.bat                # Startup script (Batch)
├── cleanup.py               # Cleanup script (Python)
├── cleanup.sh               # Cleanup script (Shell)
├── cleanup.bat              # Cleanup script (Batch)
│
├── QUICK_START.md           # Quick start guide
├── STARTUP_GUIDE.md         # Comprehensive startup guide
├── SETUP.md                 # Setup guide (Vietnamese)
├── README.md                # Project README
└── requirements.txt         # Python dependencies
```

---

## 🎯 Các Tính Năng Chính

### 1. Overview Tab 📈
- Giá tiền điện tử theo thời gian thực
- Biểu đồ 24 giờ
- Thông tin thị trường

### 2. Predictions Tab 🔮
- Dự đoán giá dài hạn (3-36 tháng)
- Dự đoán giá ngắn hạn (1-72 giờ)
- Tín hiệu giao dịch

### 3. Data Tab 📊
- Thu thập dữ liệu từ Binance
- Xử lý dữ liệu
- Lưu trữ dữ liệu

### 4. Models Tab 🤖
- Huấn luyện mô hình ML
- Đánh giá mô hình
- Cải thiện mô hình

### 5. Backtest Tab 🔄
- Kiểm tra chiến lược
- Phân tích kết quả
- Tối ưu hóa chiến lược

### 6. Futures Trading Tab 💹
- Giao dịch tương lai
- Quản lý vị trí
- P&L theo thời gian thực

### 7. Paper Trading Tab 📝
- Giao dịch giả lập
- Không sử dụng tiền thật
- Học tập an toàn

### 8. Risk Tab ⚠️
- Tính toán rủi ro
- Quản lý vị trí
- Giá thanh lý

---

## 🛠️ Công Nghệ Sử Dụng

### Backend
- **Python 3.9+**: Ngôn ngữ lập trình
- **FastAPI**: Framework REST API
- **Uvicorn**: ASGI server
- **aiohttp**: Async HTTP client
- **PyTorch**: Deep learning framework

### Frontend
- **HTML5/CSS3**: Markup & styling
- **Vanilla JavaScript**: No framework
- **Chart.js**: Data visualization
- **Axios**: HTTP client

### Database & Storage
- **JSON**: Configuration & data
- **CSV**: Data export
- **Binance API**: Real-time prices

---

## 📦 Cài Đặt Dependencies

```bash
# Tự động (khuyến nghị)
python3 start.py

# Thủ Công
pip install -r requirements.txt
```

### Dependencies Chính
- fastapi
- uvicorn
- aiohttp
- torch
- numpy
- pandas
- scikit-learn

---

## 🎮 Các Lệnh Hữu Ích

### Khởi Chạy
```bash
python3 start.py              # Khởi chạy tất cả
./start.sh                    # Shell script
start.bat                     # Batch script
```

### Dọn Dẹp
```bash
python3 cleanup.py            # Cleanup Python
./cleanup.sh                  # Shell script
cleanup.bat                   # Batch script
```

### Backend Riêng
```bash
python3 -m src.api.server
```

### Frontend Riêng
```bash
python3 frontend/server.py
```

### Kiểm Tra
```bash
curl http://localhost:8000/health
curl http://localhost:3000
```

---

## 🔐 Bảo Mật

⚠️ **QUAN TRỌNG**:
- ❌ KHÔNG sử dụng Live Trading mode với tiền thật
- ✅ Luôn sử dụng Paper Trading mode để học tập
- ✅ Kiểm tra kỹ chiến lược trước khi giao dịch thực

---

## 📊 Hỗ Trợ Tiền Điện Tử

20+ cryptocurrencies:
- **Top**: BTC, ETH, BNB, SOL, XRP
- **Layer 1**: ADA, AVAX, DOT, ATOM
- **DeFi**: UNI, LINK, AAVE, SUSHI
- **Storage**: FIL, ARWEAVE
- **Other**: DOGE, MATIC, LTC, VET, THETA, FTM

---

## 🧪 Testing

```bash
# Run tests
python3 -m pytest tests/

# Run specific test
python3 -m pytest tests/unit/test_models.py

# Run with coverage
python3 -m pytest --cov=src tests/
```

---

## 📚 Tài Liệu

- **QUICK_START.md**: Hướng dẫn khởi chạy nhanh
- **STARTUP_GUIDE.md**: Hướng dẫn khởi chạy toàn diện
- **SETUP.md**: Hướng dẫn cài đặt (Vietnamese)
- **README.md**: Tài liệu dự án
- **API Docs**: http://localhost:8000/docs

---

## 🐛 Khắc Phục Sự Cố

### Port Already in Use
```bash
# macOS/Linux
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### ModuleNotFoundError
```bash
pip install -r requirements.txt --upgrade
```

### Permission Denied
```bash
chmod +x start.sh start.py cleanup.sh cleanup.py
```

---

## 🤝 Đóng Góp

Để đóng góp:
1. Fork repository
2. Tạo branch mới
3. Commit changes
4. Push to branch
5. Tạo Pull Request

---

## 📞 Liên Hệ & Hỗ Trợ

- **GitHub**: https://github.com/PhucBaogithub/CryptoSage
- **Issues**: https://github.com/PhucBaogithub/CryptoSage/issues
- **Email**: phucbao@example.com

---

## 📝 Lịch Sử Phiên Bản

### v1.0.0 (2025-10-20)
- ✅ Khởi chạy dự án
- ✅ Tạo dashboard với 8 tab
- ✅ Tích hợp Binance API
- ✅ Thêm dự đoán giá
- ✅ Thêm giao dịch tương lai
- ✅ Thêm giao dịch giả lập
- ✅ Thêm quản lý rủi ro
- ✅ Tạo startup scripts
- ✅ Tạo cleanup scripts
- ✅ Tạo tài liệu toàn diện

---

## 📄 Giấy Phép

MIT License - Xem LICENSE file

---

## 🎯 Roadmap

### Phiên Bản Tiếp Theo
- [ ] WebSocket real-time updates
- [ ] Advanced charting (TradingView)
- [ ] Risk management alerts
- [ ] Backtesting improvements
- [ ] Mobile responsive design
- [ ] Dark mode theme
- [ ] Export functionality
- [ ] Advanced ML models

---

**Phiên Bản**: 1.0.0  
**Cập Nhật**: 2025-10-20  
**Trạng Thái**: ✅ Production Ready  
**Tác Giả**: Phuc Bao  
**Repository**: https://github.com/PhucBaogithub/CryptoSage

