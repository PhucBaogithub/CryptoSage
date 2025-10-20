/**
 * Bitcoin Futures Trading Dashboard - Main Application
 */

const API_BASE_URL = 'http://localhost:8000/api';

// Chart instances
let equityChart = null;
let returnsChart = null;
let winrateChart = null;
let drawdownChart = null;
let backtestEquityChart = null;
let monthlyReturnsChart = null;
let dataDistributionChart = null;
let coinComparisonChart = null;
let ltPredictionsChart = null;
let stPredictionsChart = null;
let modelPerformanceChart = null;
let trainingHistoryChart = null;
let positionDistributionChart = null;
let realtimePnlChart = null;
let tradingActivityChart = null;
let riskGaugeChart = null;
let liquidationRiskChart = null;
let fundingCostChart = null;

// Chart colors
const chartColors = {
    primary: '#3498db',
    success: '#27ae60',
    danger: '#e74c3c',
    warning: '#f39c12',
    light: '#ecf0f1',
    dark: '#2c3e50'
};

// ============================================================================
// Initialization
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    try {
        initializeApp();
        setupEventListeners();
        loadInitialData();
        connectWebSocket();

        // Retry status update every 5 seconds
        setInterval(updateSystemStatus, 5000);
    } catch (error) {
        console.error('Error during initialization:', error);
    }
});

function initializeApp() {
    console.log('Initializing Bitcoin Futures Trading Dashboard');
    // Call updateSystemStatus after a short delay to ensure DOM is ready
    setTimeout(updateSystemStatus, 100);
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

    // Initialize charts based on tab
    setTimeout(() => {
        if (tabName === 'overview') {
            if (!equityChart) initializeEquityChart();
            if (!returnsChart) initializeReturnsChart();
            if (!winrateChart) initializeWinrateChart();
            if (!drawdownChart) initializeDrawdownChart();
        } else if (tabName === 'data') {
            if (!dataDistributionChart) initializeDataDistributionChart();
            if (!coinComparisonChart) initializeCoinComparisonChart();
        } else if (tabName === 'models') {
            if (!ltPredictionsChart) initializeLTPredictionsChart();
            if (!stPredictionsChart) initializeSTPredictionsChart();
            if (!modelPerformanceChart) initializeModelPerformanceChart();
            if (!trainingHistoryChart) initializeTrainingHistoryChart();
        } else if (tabName === 'backtest') {
            if (!backtestEquityChart) initializeBacktestEquityChart();
            if (!monthlyReturnsChart) initializeMonthlyReturnsChart();
        } else if (tabName === 'trading') {
            if (!positionDistributionChart) initializePositionDistributionChart();
            if (!realtimePnlChart) initializeRealtimePnlChart();
            if (!tradingActivityChart) initializeTradingActivityChart();
        } else if (tabName === 'risk') {
            if (!riskGaugeChart) initializeRiskGaugeChart();
            if (!liquidationRiskChart) initializeLiquidationRiskChart();
            if (!fundingCostChart) initializeFundingCostChart();
        }
    }, 100);
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
    try {
        const status = await apiCall('/status');
        const indicator = document.getElementById('status-indicator');
        const text = document.getElementById('status-text');

        if (indicator && text) {
            if (status) {
                indicator.style.backgroundColor = '#27ae60';
                text.textContent = 'Connected';
            } else {
                indicator.style.backgroundColor = '#e74c3c';
                text.textContent = 'Disconnected';
            }
        }
    } catch (error) {
        console.error('Failed to update system status:', error);
    }
}

async function loadInitialData() {
    try {
        // Load account info
        const account = await apiCall('/trading/account');
        if (account) {
            const balanceEl = document.getElementById('balance');
            const equityEl = document.getElementById('equity');
            const pnlEl = document.getElementById('unrealized-pnl');
            const marginEl = document.getElementById('margin-ratio');

            if (balanceEl) balanceEl.textContent = `$${account.balance.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
            if (equityEl) equityEl.textContent = `$${account.equity.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
            if (pnlEl) pnlEl.textContent = `${account.unrealized_pnl >= 0 ? '+' : ''}$${account.unrealized_pnl.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
            if (marginEl) marginEl.textContent = `${(account.margin_ratio * 100).toFixed(1)}%`;
        }
    } catch (error) {
        console.error('Error loading account info:', error);
    }

    try {
        // Load positions
        const positions = await apiCall('/trading/positions');
        if (positions && positions.positions && positions.positions.length > 0) {
            updatePositionsTable(positions.positions);
        }
    } catch (error) {
        console.error('Error loading positions:', error);
    }

    try {
        // Load backtest results
        const results = await apiCall('/backtest/results');
        if (results) {
            updateBacktestResults(results);
        }
    } catch (error) {
        console.error('Error loading backtest results:', error);
    }

    try {
        // Load model status
        const modelStatus = await apiCall('/models/status');
        if (modelStatus) {
            const ltStatusEl = document.getElementById('lt-status');
            const ltAccuracyEl = document.getElementById('lt-accuracy');
            const ltLossEl = document.getElementById('lt-loss');
            const stStatusEl = document.getElementById('st-status');
            const stAccuracyEl = document.getElementById('st-accuracy');
            const stLossEl = document.getElementById('st-loss');

            if (ltStatusEl) ltStatusEl.textContent = modelStatus.long_term.status;
            if (ltAccuracyEl) ltAccuracyEl.textContent = `${(modelStatus.long_term.accuracy * 100).toFixed(0)}%`;
            if (ltLossEl) ltLossEl.textContent = modelStatus.long_term.loss.toFixed(4);
            if (stStatusEl) stStatusEl.textContent = modelStatus.short_term.status;
            if (stAccuracyEl) stAccuracyEl.textContent = `${(modelStatus.short_term.accuracy * 100).toFixed(0)}%`;
            if (stLossEl) stLossEl.textContent = modelStatus.short_term.loss.toFixed(4);
        }
    } catch (error) {
        console.error('Error loading model status:', error);
    }

    try {
        // Load predictions
        const predictions = await apiCall('/models/predictions');
        if (predictions) {
            const elem1 = document.querySelector('[data-tab="models"] .grid-2 div:nth-child(1) .metric:nth-child(1) .value');
            const elem2 = document.querySelector('[data-tab="models"] .grid-2 div:nth-child(1) .metric:nth-child(2) .value');
            const elem3 = document.querySelector('[data-tab="models"] .grid-2 div:nth-child(1) .metric:nth-child(3) .value');

            if (elem1) elem1.textContent = `${(predictions.long_term.mean * 100).toFixed(2)}%`;
            if (elem2) elem2.textContent = `${(predictions.long_term.std * 100).toFixed(2)}%`;
            if (elem3) elem3.textContent = `${(predictions.long_term.confidence * 100).toFixed(0)}%`;
        }
    } catch (error) {
        console.error('Error loading predictions:', error);
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
    const result = await apiCall(`/api/trading/start?mode=${mode}`, 'POST');
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
                borderColor: chartColors.primary,
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: '#e0e0e0'
                    },
                    ticks: {
                        color: '#666666'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#666666'
                    }
                }
            }
        }
    });
}

function initializeReturnsChart() {
    const ctx = document.getElementById('returns-chart');
    if (!ctx) return;
    returnsChart = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
            datasets: [{
                label: 'Daily Returns %',
                data: Array.from({length: 30}, () => (Math.random() - 0.5) * 4),
                backgroundColor: chartColors.success,
                borderColor: chartColors.success,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: '#e0e0e0' }, ticks: { color: '#666666' } },
                x: { grid: { display: false }, ticks: { color: '#666666' } }
            }
        }
    });
}

function initializeWinrateChart() {
    const ctx = document.getElementById('winrate-chart');
    if (!ctx) return;
    winrateChart = new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['Wins', 'Losses'],
            datasets: [{
                data: [58.33, 41.67],
                backgroundColor: [chartColors.success, chartColors.danger],
                borderColor: '#ffffff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

function initializeDrawdownChart() {
    const ctx = document.getElementById('drawdown-chart');
    if (!ctx) return;
    drawdownChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
            datasets: [{
                label: 'Drawdown %',
                data: Array.from({length: 30}, (_, i) => -Math.random() * 10),
                borderColor: chartColors.danger,
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: '#e0e0e0' }, ticks: { color: '#666666' } },
                x: { grid: { display: false }, ticks: { color: '#666666' } }
            }
        }
    });
}

function initializeBacktestEquityChart() {
    const ctx = document.getElementById('backtest-equity-chart');
    if (!ctx) return;
    backtestEquityChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: Array.from({length: 100}, (_, i) => `${i}`),
            datasets: [{
                label: 'Equity',
                data: Array.from({length: 100}, (_, i) => 100000 * Math.pow(1.001, i)),
                borderColor: chartColors.primary,
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: false, grid: { color: '#e0e0e0' }, ticks: { color: '#666666' } },
                x: { grid: { display: false }, ticks: { color: '#666666' } }
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

function initializeMonthlyReturnsChart() {
    const ctx = document.getElementById('monthly-returns-chart');
    if (!ctx) return;
    monthlyReturnsChart = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Monthly Returns %',
                data: [2.5, 3.1, -1.2, 4.5, 2.8, 1.9, 3.2, 2.1, -0.5, 3.8, 2.4, 1.7],
                backgroundColor: chartColors.success,
                borderColor: chartColors.success,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: '#e0e0e0' }, ticks: { color: '#666666' } },
                x: { grid: { display: false }, ticks: { color: '#666666' } }
            }
        }
    });
}

function initializeDataDistributionChart() {
    const ctx = document.getElementById('data-distribution-chart');
    if (!ctx) return;
    dataDistributionChart = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%'],
            datasets: [{
                label: 'Data Points',
                data: [45, 52, 48, 61, 55, 67, 59, 72, 64, 58],
                backgroundColor: chartColors.primary,
                borderColor: chartColors.primary,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: '#e0e0e0' }, ticks: { color: '#666666' } },
                x: { grid: { display: false }, ticks: { color: '#666666' } }
            }
        }
    });
}

function initializeCoinComparisonChart() {
    const ctx = document.getElementById('coin-comparison-chart');
    if (!ctx) return;
    coinComparisonChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
            datasets: [
                {
                    label: 'BTC',
                    data: Array.from({length: 30}, (_, i) => 45000 + (i * 100)),
                    borderColor: '#f7931a',
                    backgroundColor: 'rgba(247, 147, 26, 0.1)',
                    tension: 0.4,
                    borderWidth: 2
                },
                {
                    label: 'ETH',
                    data: Array.from({length: 30}, (_, i) => 2500 + (i * 10)),
                    borderColor: '#627eea',
                    backgroundColor: 'rgba(98, 126, 234, 0.1)',
                    tension: 0.4,
                    borderWidth: 2
                },
                {
                    label: 'BNB',
                    data: Array.from({length: 30}, (_, i) => 600 + (i * 2)),
                    borderColor: '#f3ba2f',
                    backgroundColor: 'rgba(243, 186, 47, 0.1)',
                    tension: 0.4,
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } },
            scales: {
                y: { grid: { color: '#e0e0e0' }, ticks: { color: '#666666' } },
                x: { grid: { display: false }, ticks: { color: '#666666' } }
            }
        }
    });
}

function initializeLTPredictionsChart() {
    const ctx = document.getElementById('lt-predictions-chart');
    if (!ctx) return;
    ltPredictionsChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
            datasets: [{
                label: 'Predicted Price',
                data: Array.from({length: 30}, (_, i) => 45000 + (i * 150)),
                borderColor: chartColors.primary,
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                tension: 0.4,
                fill: true,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: '#e0e0e0' }, ticks: { color: '#666666' } },
                x: { grid: { display: false }, ticks: { color: '#666666' } }
            }
        }
    });
}

function initializeSTPredictionsChart() {
    const ctx = document.getElementById('st-predictions-chart');
    if (!ctx) return;
    stPredictionsChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: Array.from({length: 24}, (_, i) => `${i}:00`),
            datasets: [{
                label: 'Predicted Price',
                data: Array.from({length: 24}, (_, i) => 45000 + (i * 50)),
                borderColor: chartColors.warning,
                backgroundColor: 'rgba(243, 156, 18, 0.1)',
                tension: 0.4,
                fill: true,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: '#e0e0e0' }, ticks: { color: '#666666' } },
                x: { grid: { display: false }, ticks: { color: '#666666' } }
            }
        }
    });
}

function initializeModelPerformanceChart() {
    const ctx = document.getElementById('model-performance-chart');
    if (!ctx) return;
    modelPerformanceChart = new Chart(ctx.getContext('2d'), {
        type: 'radar',
        data: {
            labels: ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC'],
            datasets: [{
                label: 'Model Performance',
                data: [85, 82, 88, 85, 87],
                borderColor: chartColors.primary,
                backgroundColor: 'rgba(52, 152, 219, 0.2)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

function initializeTrainingHistoryChart() {
    const ctx = document.getElementById('training-history-chart');
    if (!ctx) return;
    trainingHistoryChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: Array.from({length: 50}, (_, i) => `Epoch ${i+1}`),
            datasets: [
                {
                    label: 'Training Loss',
                    data: Array.from({length: 50}, (_, i) => 0.5 * Math.exp(-i/10)),
                    borderColor: chartColors.danger,
                    backgroundColor: 'rgba(231, 76, 60, 0.1)',
                    tension: 0.4,
                    borderWidth: 2
                },
                {
                    label: 'Validation Loss',
                    data: Array.from({length: 50}, (_, i) => 0.52 * Math.exp(-i/10)),
                    borderColor: chartColors.warning,
                    backgroundColor: 'rgba(243, 156, 18, 0.1)',
                    tension: 0.4,
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } },
            scales: {
                y: { grid: { color: '#e0e0e0' }, ticks: { color: '#666666' } },
                x: { grid: { display: false }, ticks: { color: '#666666' } }
            }
        }
    });
}

function initializePositionDistributionChart() {
    const ctx = document.getElementById('position-distribution-chart');
    if (!ctx) return;
    positionDistributionChart = new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['BTC', 'ETH', 'BNB', 'SOL', 'XRP'],
            datasets: [{
                data: [40, 25, 20, 10, 5],
                backgroundColor: ['#f7931a', '#627eea', '#f3ba2f', '#14f195', '#23292f'],
                borderColor: '#ffffff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

function initializeRealtimePnlChart() {
    const ctx = document.getElementById('realtime-pnl-chart');
    if (!ctx) return;
    realtimePnlChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: Array.from({length: 60}, (_, i) => `${i}m`),
            datasets: [{
                label: 'P&L ($)',
                data: Array.from({length: 60}, (_, i) => (Math.random() - 0.5) * 1000),
                borderColor: chartColors.success,
                backgroundColor: 'rgba(39, 174, 96, 0.1)',
                tension: 0.4,
                fill: true,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: '#e0e0e0' }, ticks: { color: '#666666' } },
                x: { grid: { display: false }, ticks: { color: '#666666' } }
            }
        }
    });
}

function initializeTradingActivityChart() {
    const ctx = document.getElementById('trading-activity-chart');
    if (!ctx) return;
    tradingActivityChart = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: Array.from({length: 24}, (_, i) => `${i}:00`),
            datasets: [{
                label: 'Trades',
                data: Array.from({length: 24}, () => Math.floor(Math.random() * 10)),
                backgroundColor: chartColors.primary,
                borderColor: chartColors.primary,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: '#e0e0e0' }, ticks: { color: '#666666' } },
                x: { grid: { display: false }, ticks: { color: '#666666' } }
            }
        }
    });
}

function initializeRiskGaugeChart() {
    const ctx = document.getElementById('risk-gauge-chart');
    if (!ctx) return;
    riskGaugeChart = new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['Safe', 'Moderate', 'High'],
            datasets: [{
                data: [60, 30, 10],
                backgroundColor: [chartColors.success, chartColors.warning, chartColors.danger],
                borderColor: '#ffffff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

function initializeLiquidationRiskChart() {
    const ctx = document.getElementById('liquidation-risk-chart');
    if (!ctx) return;
    liquidationRiskChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
            datasets: [{
                label: 'Distance to Liquidation %',
                data: Array.from({length: 30}, (_, i) => 30 + (Math.random() - 0.5) * 10),
                borderColor: chartColors.danger,
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                tension: 0.4,
                fill: true,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: '#e0e0e0' }, ticks: { color: '#666666' } },
                x: { grid: { display: false }, ticks: { color: '#666666' } }
            }
        }
    });
}

function initializeFundingCostChart() {
    const ctx = document.getElementById('funding-cost-chart');
    if (!ctx) return;
    fundingCostChart = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
            datasets: [{
                label: 'Daily Funding Cost ($)',
                data: Array.from({length: 30}, () => Math.random() * 200),
                backgroundColor: chartColors.warning,
                borderColor: chartColors.warning,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: '#e0e0e0' }, ticks: { color: '#666666' } },
                x: { grid: { display: false }, ticks: { color: '#666666' } }
            }
        }
    });
}

// ============================================================================
// WebSocket
// ============================================================================

function connectWebSocket() {
    try {
        // WebSocket endpoint is optional - gracefully handle if not available
        const ws = new WebSocket('ws://localhost:8000/api/ws/market-data');

        ws.onopen = () => {
            console.log('WebSocket connected');
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data.type === 'market_data') {
                    // Update market data in real-time
                    console.log('Market data:', data);
                }
            } catch (e) {
                console.error('Failed to parse WebSocket message:', e);
            }
        };

        ws.onerror = (error) => {
            console.warn('WebSocket error (non-critical):', error);
        };

        ws.onclose = () => {
            console.log('WebSocket disconnected');
        };
    } catch (error) {
        console.warn('WebSocket connection failed (non-critical):', error);
    }
}

// ============================================================================
// Utilities
// ============================================================================

function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // Could be enhanced with a toast notification library
}

