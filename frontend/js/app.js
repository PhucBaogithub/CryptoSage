/**
 * Bitcoin Futures Trading Dashboard - Main Application
 */

const API_BASE_URL = 'http://localhost:8000/api';
let equityChart = null;
let backtestEquityChart = null;

// ============================================================================
// Initialization
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    loadInitialData();
    connectWebSocket();
});

function initializeApp() {
    console.log('Initializing Bitcoin Futures Trading Dashboard');
    updateSystemStatus();
}

function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            switchTab(e.target.dataset.tab);
        });
    });
}

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Add active class to clicked button
    event.target.classList.add('active');

    // Initialize charts if needed
    if (tabName === 'overview' && !equityChart) {
        initializeEquityChart();
    }
    if (tabName === 'backtest' && !backtestEquityChart) {
        initializeBacktestEquityChart();
    }
}

// ============================================================================
// API Calls
// ============================================================================

async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        const response = await axios({
            method,
            url: `${API_BASE_URL}${endpoint}`,
            data,
            headers: {
                'Content-Type': 'application/json',
            }
        });

        return response.data;
    } catch (error) {
        console.error(`API Error: ${endpoint}`, error);
        showNotification('Error: ' + error.message, 'error');
        return null;
    }
}

// ============================================================================
// System Status
// ============================================================================

async function updateSystemStatus() {
    const status = await apiCall('/status');
    if (status) {
        document.getElementById('status-indicator').style.backgroundColor = '#000000';
        document.getElementById('status-text').textContent = 'Connected';
    }
}

async function loadInitialData() {
    // Load account info
    const account = await apiCall('/trading/account');
    if (account) {
        document.getElementById('balance').textContent = `$${account.balance.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('equity').textContent = `$${account.equity.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('unrealized-pnl').textContent = `${account.unrealized_pnl >= 0 ? '+' : ''}$${account.unrealized_pnl.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('margin-ratio').textContent = `${(account.margin_ratio * 100).toFixed(1)}%`;
    }

    // Load positions
    const positions = await apiCall('/trading/positions');
    if (positions && positions.positions.length > 0) {
        updatePositionsTable(positions.positions);
    }

    // Load backtest results
    const results = await apiCall('/backtest/results');
    if (results) {
        updateBacktestResults(results);
    }

    // Load model status
    const modelStatus = await apiCall('/models/status');
    if (modelStatus) {
        document.getElementById('lt-status').textContent = modelStatus.long_term.status;
        document.getElementById('lt-accuracy').textContent = `${(modelStatus.long_term.accuracy * 100).toFixed(0)}%`;
        document.getElementById('lt-loss').textContent = modelStatus.long_term.loss.toFixed(4);
        document.getElementById('st-status').textContent = modelStatus.short_term.status;
        document.getElementById('st-accuracy').textContent = `${(modelStatus.short_term.accuracy * 100).toFixed(0)}%`;
        document.getElementById('st-loss').textContent = modelStatus.short_term.loss.toFixed(4);
    }

    // Load predictions
    const predictions = await apiCall('/models/predictions');
    if (predictions) {
        document.querySelector('[data-tab="models"] .grid-2 div:nth-child(1) .metric:nth-child(1) .value').textContent = `${(predictions.long_term.mean * 100).toFixed(2)}%`;
        document.querySelector('[data-tab="models"] .grid-2 div:nth-child(1) .metric:nth-child(2) .value').textContent = `${(predictions.long_term.std * 100).toFixed(2)}%`;
        document.querySelector('[data-tab="models"] .grid-2 div:nth-child(1) .metric:nth-child(3) .value').textContent = `${(predictions.long_term.confidence * 100).toFixed(0)}%`;
    }
}

// ============================================================================
// Data Collection
// ============================================================================

async function collectData() {
    const symbols = document.getElementById('symbols-input').value.split(',').map(s => s.trim());
    const timeframes = Array.from(document.getElementById('timeframes-select').selectedOptions).map(o => o.value);
    const limit = parseInt(document.getElementById('limit-input').value);

    const result = await apiCall('/data/collect', 'POST', {
        symbols,
        timeframes,
        limit
    });

    if (result) {
        showNotification('Data collection started', 'success');
    }
}

// ============================================================================
// Model Training
// ============================================================================

async function trainModels() {
    const result = await apiCall('/models/train?symbol=BTCUSDT', 'POST');
    if (result) {
        showNotification('Model training started', 'success');
    }
}

// ============================================================================
// Backtesting
// ============================================================================

async function runBacktest() {
    const symbol = document.getElementById('backtest-symbol').value;
    const timeframe = document.getElementById('backtest-timeframe').value;
    const startDate = document.getElementById('backtest-start').value;
    const endDate = document.getElementById('backtest-end').value;
    const capital = parseFloat(document.getElementById('backtest-capital').value);

    const result = await apiCall('/backtest/run', 'POST', {
        symbol,
        timeframe,
        start_date: startDate,
        end_date: endDate,
        initial_capital: capital
    });

    if (result) {
        showNotification('Backtest started', 'success');
        setTimeout(() => {
            loadBacktestResults();
        }, 2000);
    }
}

async function loadBacktestResults() {
    const results = await apiCall('/backtest/results');
    if (results) {
        updateBacktestResults(results);
    }

    const trades = await apiCall('/backtest/trades');
    if (trades) {
        updateTradesTable(trades.trades);
    }

    const equity = await apiCall('/backtest/equity-curve');
    if (equity) {
        updateBacktestEquityChart(equity.equity_curve);
    }
}

function updateBacktestResults(results) {
    document.querySelectorAll('[data-tab="backtest"] .card:nth-child(2) .grid-2 .metric').forEach((metric, index) => {
        const keys = ['total_return_pct', 'annual_return_pct', 'sharpe_ratio', 'max_drawdown_pct', 'win_rate_pct', 'profit_factor'];
        const value = results[keys[index]];
        metric.querySelector('.value').textContent = typeof value === 'number' ? value.toFixed(2) : value;
    });
}

function updateTradesTable(trades) {
    const tbody = document.getElementById('trades-table');
    tbody.innerHTML = trades.map(trade => `
        <tr>
            <td>${trade.entry_time}</td>
            <td>${trade.exit_time}</td>
            <td>${trade.side}</td>
            <td>$${trade.entry_price.toLocaleString()}</td>
            <td>$${trade.exit_price.toLocaleString()}</td>
            <td class="${trade.pnl >= 0 ? 'positive' : 'negative'}">$${trade.pnl.toLocaleString()}</td>
            <td class="${trade.pnl_pct >= 0 ? 'positive' : 'negative'}">${trade.pnl_pct >= 0 ? '+' : ''}${trade.pnl_pct.toFixed(2)}%</td>
        </tr>
    `).join('');
}

// ============================================================================
// Trading
// ============================================================================

async function startTrading() {
    const mode = document.getElementById('trading-mode').value;
    const result = await apiCall(`/trading/start?mode=${mode}`, 'POST');
    if (result) {
        showNotification(`Trading started in ${mode} mode`, 'success');
    }
}

async function stopTrading() {
    const result = await apiCall('/trading/stop', 'POST');
    if (result) {
        showNotification('Trading stopped', 'success');
    }
}

async function placeOrder() {
    const symbol = document.getElementById('order-symbol').value;
    const side = document.getElementById('order-side').value;
    const size = parseFloat(document.getElementById('order-size').value);
    const leverage = parseFloat(document.getElementById('order-leverage').value);
    const mode = document.getElementById('trading-mode').value;

    const result = await apiCall('/trading/place-order', 'POST', {
        symbol,
        side,
        size,
        leverage,
        mode
    });

    if (result) {
        showNotification(`Order placed: ${side} ${size} ${symbol}`, 'success');
    }
}

function updatePositionsTable(positions) {
    const tbody = document.getElementById('positions-table');
    tbody.innerHTML = positions.map(pos => `
        <tr>
            <td>${pos.symbol}</td>
            <td>${pos.side}</td>
            <td>${pos.size}</td>
            <td>$${pos.entry_price.toLocaleString()}</td>
            <td>$${pos.current_price.toLocaleString()}</td>
            <td class="${pos.pnl >= 0 ? 'positive' : 'negative'}">$${pos.pnl.toLocaleString()}</td>
            <td class="${pos.pnl_pct >= 0 ? 'positive' : 'negative'}">${pos.pnl_pct >= 0 ? '+' : ''}${pos.pnl_pct.toFixed(2)}%</td>
        </tr>
    `).join('');
}

// ============================================================================
// Risk Management
// ============================================================================

async function calculateRiskMetrics() {
    const entryPrice = parseFloat(document.getElementById('risk-entry-price').value);
    const currentPrice = parseFloat(document.getElementById('risk-current-price').value);
    const positionSize = parseFloat(document.getElementById('risk-position-size').value);
    const leverage = parseFloat(document.getElementById('risk-leverage').value);
    const fundingRate = parseFloat(document.getElementById('risk-funding-rate').value);

    const result = await apiCall('/risk/metrics', 'POST', {
        entry_price: entryPrice,
        current_price: currentPrice,
        position_size_usd: positionSize,
        leverage,
        funding_rate: fundingRate,
        volatility: 0.25
    });

    if (result) {
        document.getElementById('liq-price').textContent = `$${result.liquidation_price.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('liq-distance').textContent = `${result.liquidation_distance_pct.toFixed(2)}%`;
        document.getElementById('max-loss-usd').textContent = `-$${result.max_loss_usd.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('max-loss-pct').textContent = `-${result.max_loss_pct.toFixed(2)}%`;
        document.getElementById('funding-hourly').textContent = `$${result.funding_cost_hourly.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('funding-daily').textContent = `$${result.funding_cost_daily.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
    }
}

// ============================================================================
// Charts
// ============================================================================

function initializeEquityChart() {
    const ctx = document.getElementById('equity-chart').getContext('2d');
    equityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
            datasets: [{
                label: 'Equity',
                data: Array.from({length: 30}, (_, i) => 100000 + (i * 500)),
                borderColor: '#000000',
                backgroundColor: 'rgba(0, 0, 0, 0.05)',
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: '#333333'
                    },
                    ticks: {
                        color: '#cccccc'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#cccccc'
                    }
                }
            }
        }
    });
}

function initializeBacktestEquityChart() {
    const ctx = document.getElementById('backtest-equity-chart').getContext('2d');
    backtestEquityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: 100}, (_, i) => `${i}`),
            datasets: [{
                label: 'Equity',
                data: Array.from({length: 100}, (_, i) => 100000 * Math.pow(1.001, i)),
                borderColor: '#000000',
                backgroundColor: 'rgba(0, 0, 0, 0.05)',
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: '#333333'
                    },
                    ticks: {
                        color: '#cccccc'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#cccccc'
                    }
                }
            }
        }
    });
}

function updateBacktestEquityChart(equityData) {
    if (backtestEquityChart) {
        backtestEquityChart.data.labels = equityData.map((_, i) => `${i}`);
        backtestEquityChart.data.datasets[0].data = equityData.map(e => e.value);
        backtestEquityChart.update();
    }
}

// ============================================================================
// WebSocket
// ============================================================================

function connectWebSocket() {
    try {
        const ws = new WebSocket('ws://localhost:8000/ws/market-data');
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'market_data') {
                // Update market data in real-time
                console.log('Market data:', data);
            }
        };
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    } catch (error) {
        console.error('WebSocket connection failed:', error);
    }
}

// ============================================================================
// Utilities
// ============================================================================

function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // Could be enhanced with a toast notification library
}

