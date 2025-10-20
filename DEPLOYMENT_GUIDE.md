# Deployment Guide

Complete guide for deploying the Bitcoin Futures Trading System to production.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [GitHub Setup](#github-setup)
5. [Monitoring & Maintenance](#monitoring--maintenance)

## Local Development

### Quick Start

```bash
# 1. Clone repository
cd /Users/phucbao/Documents/Binance

# 2. Install dependencies
pip install -e .

# 3. Configure environment
cp .env.example .env
# Edit .env with your settings

# 4. Start backend (Terminal 1)
python -m src.api.server

# 5. Start frontend (Terminal 2)
cd frontend && python server.py

# 6. Open dashboard
# http://localhost:3000
```

### Running Tests

```bash
pytest tests/
pytest tests/ --cov=src
pytest tests/unit/test_risk_management.py -v
```

### Running Examples

```bash
python examples/01_data_collection.py
python examples/02_feature_engineering.py
python examples/03_model_training.py
python examples/04_backtesting.py
python examples/05_risk_management.py
```

## Docker Deployment

### Build Docker Image

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Expose ports
EXPOSE 8000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start services
CMD ["sh", "-c", "python -m src.api.server & cd frontend && python server.py"]
```

### Build and Run

```bash
# Build image
docker build -t bitcoin-trading-dashboard:latest .

# Run container
docker run -d \
  --name bitcoin-trading \
  -p 8000:8000 \
  -p 3000:3000 \
  -e BINANCE_API_KEY=your_key \
  -e BINANCE_API_SECRET=your_secret \
  -v /path/to/data:/app/data \
  -v /path/to/logs:/app/logs \
  bitcoin-trading-dashboard:latest

# View logs
docker logs -f bitcoin-trading

# Stop container
docker stop bitcoin-trading
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - BINANCE_API_KEY=${BINANCE_API_KEY}
      - BINANCE_API_SECRET=${BINANCE_API_SECRET}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - api
    restart: unless-stopped

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
      - frontend
    restart: unless-stopped
```

Run with Docker Compose:

```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## Cloud Deployment

### AWS EC2

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t3.medium (minimum)
   - Security group: Allow ports 80, 443, 8000, 3000

2. **Connect and Setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   
   # Update system
   sudo apt-get update && sudo apt-get upgrade -y
   
   # Install dependencies
   sudo apt-get install -y python3.10 python3-pip git
   
   # Clone repository
   git clone https://github.com/YOUR_USERNAME/bitcoin-futures-trading.git
   cd bitcoin-futures-trading
   
   # Install project
   pip install -e .
   ```

3. **Setup Systemd Services**
   
   Create `/etc/systemd/system/bitcoin-api.service`:
   ```ini
   [Unit]
   Description=Bitcoin Trading API
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/bitcoin-futures-trading
   ExecStart=/usr/bin/python3 -m src.api.server
   Restart=always
   RestartSec=10
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   Create `/etc/systemd/system/bitcoin-frontend.service`:
   ```ini
   [Unit]
   Description=Bitcoin Trading Frontend
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/bitcoin-futures-trading/frontend
   ExecStart=/usr/bin/python3 server.py
   Restart=always
   RestartSec=10
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable bitcoin-api bitcoin-frontend
   sudo systemctl start bitcoin-api bitcoin-frontend
   sudo systemctl status bitcoin-api bitcoin-frontend
   ```

### Heroku

1. **Create Heroku App**
   ```bash
   heroku create bitcoin-trading-app
   ```

2. **Set Environment Variables**
   ```bash
   heroku config:set BINANCE_API_KEY=your_key
   heroku config:set BINANCE_API_SECRET=your_secret
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

### Google Cloud Run

1. **Build and Push Image**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/bitcoin-trading
   ```

2. **Deploy**
   ```bash
   gcloud run deploy bitcoin-trading \
     --image gcr.io/PROJECT_ID/bitcoin-trading \
     --platform managed \
     --region us-central1 \
     --set-env-vars BINANCE_API_KEY=your_key,BINANCE_API_SECRET=your_secret
   ```

## GitHub Setup

### Initial Setup

```bash
cd /Users/phucbao/Documents/Binance

# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/bitcoin-futures-trading.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Subsequent Updates

```bash
# Make changes
git add .
git commit -m "Description of changes"
git push
```

See [GITHUB_SETUP.md](GITHUB_SETUP.md) for detailed instructions.

## Monitoring & Maintenance

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# System status
curl http://localhost:8000/api/status

# Frontend
curl http://localhost:3000
```

### Logs

```bash
# API logs (if running in foreground)
# Check console output

# Frontend logs
# Check console output

# System logs (if using systemd)
sudo journalctl -u bitcoin-api -f
sudo journalctl -u bitcoin-frontend -f
```

### Performance Monitoring

```bash
# CPU and memory
top

# Network connections
netstat -an | grep 8000

# Disk usage
df -h
```

### Backup

```bash
# Backup data
tar -czf backup-$(date +%Y%m%d).tar.gz data/ logs/ models/

# Backup database (if using)
pg_dump database_name > backup.sql
```

### Updates

```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies
pip install -e .

# Restart services
sudo systemctl restart bitcoin-api bitcoin-frontend
```

## Security Checklist

- [ ] Use HTTPS instead of HTTP
- [ ] Set strong API keys and secrets
- [ ] Use environment variables for sensitive data
- [ ] Enable firewall rules
- [ ] Use SSL certificates
- [ ] Implement rate limiting
- [ ] Add authentication
- [ ] Enable logging and monitoring
- [ ] Regular backups
- [ ] Keep dependencies updated

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

### API Not Responding

```bash
# Check if running
curl http://localhost:8000/health

# Check logs
docker logs bitcoin-trading
```

### High Memory Usage

```bash
# Check memory
free -h

# Restart services
docker restart bitcoin-trading
```

### Database Connection Issues

```bash
# Check database
psql -U user -d database -c "SELECT 1"

# Restart database
sudo systemctl restart postgresql
```

## Performance Optimization

1. **Use production ASGI server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.api.server:app
   ```

2. **Enable caching**
   - Redis for API responses
   - Browser caching for static files

3. **Use CDN**
   - CloudFlare for static content
   - AWS CloudFront for distribution

4. **Database optimization**
   - Add indexes
   - Use connection pooling
   - Archive old data

## Next Steps

1. **Set up monitoring**: Prometheus, Grafana
2. **Add authentication**: JWT, OAuth
3. **Implement CI/CD**: GitHub Actions
4. **Set up alerts**: PagerDuty, Slack
5. **Performance testing**: Load testing, stress testing

---

**Your system is ready for production deployment! 🚀**

