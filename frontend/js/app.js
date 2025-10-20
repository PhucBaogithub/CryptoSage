/**
 * Bitcoin Futures Trading Dashboard - Main Application
 */

const API_BASE_URL = 'http://localhost:8000/api';

// Real-time price data
let currentPrices = {};
let priceUpdateInterval = null;
let lastPriceUpdate = null;

// Supported cryptocurrencies
const SUPPORTED_COINS = [
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT',
    'ADAUSDT', 'AVAXUSDT', 'DOTUSDT', 'ATOMUSDT',
    'UNIUSDT', 'LINKUSDT', 'AAVEUSDT', 'SUSHIUSDT',
    'FILUSDT', 'ARWEAVEUSDT',
    'DOGEUSDT', 'MATICUSDT', 'LTCUSDT', 'VETUSDT', 'THETAUSDT', 'FTMUSDT'
];

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
let longTermPredictionsChart = null;
let shortTermPredictionsChart = null;

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

        // Start real-time price updates every 30 seconds
        startPriceUpdates();

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
// Real-time Price Updates
// ============================================================================

function startPriceUpdates() {
    // Fetch prices immediately
    updateAllPrices();

    // Then update every 30 seconds
    if (priceUpdateInterval) clearInterval(priceUpdateInterval);
    priceUpdateInterval = setInterval(updateAllPrices, 30000);
}

async function updateAllPrices() {
    try {
        const symbolsStr = SUPPORTED_COINS.join(',');
        const response = await axios.get(`${API_BASE_URL}/prices/current?symbols=${symbolsStr}`);

        if (response.data.status === 'success') {
            currentPrices = response.data.prices;
            lastPriceUpdate = new Date();

            // Update UI with new prices
            updatePriceDisplays();
            updatePaperTradingPrices();
            updatePredictionsPrices();
            updateFuturesTradingPrices();

            // Update last update time
            updateLastUpdateTime();
        }
    } catch (error) {
        console.error('Error updating prices:', error);
    }
}

function updatePriceDisplays() {
    // Update all price displays across the dashboard
    Object.entries(currentPrices).forEach(([symbol, data]) => {
        if (data.price) {
            const priceElements = document.querySelectorAll(`[data-price-symbol="${symbol}"]`);
            priceElements.forEach(el => {
                el.textContent = `$${parseFloat(data.price).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
            });
        }
    });
}

function updatePaperTradingPrices() {
    // Update paper trading position P&L based on current prices
    if (paperTradingData && paperTradingData.positions) {
        paperTradingData.positions.forEach(position => {
            const priceData = currentPrices[position.symbol];
            if (priceData && priceData.price) {
                position.current_price = parseFloat(priceData.price);
                position.pnl = (position.current_price - position.entry_price) * position.size * (position.side === 'long' ? 1 : -1);
            }
        });
        updatePaperTradingUI();
    }
}

function updatePredictionsPrices() {
    // Update current price display in predictions tab
    const selectedCoin = document.getElementById('predictions-coin-select');
    if (selectedCoin) {
        const symbol = selectedCoin.value;
        const priceData = currentPrices[symbol];
        if (priceData && priceData.price) {
            const priceDisplay = document.getElementById('current-price-display');
            if (priceDisplay) {
                priceDisplay.textContent = `$${parseFloat(priceData.price).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
            }
        }
    }
}

function updateFuturesTradingPrices() {
    // Update current price display in futures trading tab
    const selectedSymbol = document.getElementById('order-symbol');
    if (selectedSymbol) {
        const symbol = selectedSymbol.value;
        const priceData = currentPrices[symbol];
        if (priceData && priceData.price) {
            const priceDisplay = document.getElementById('current-market-price');
            if (priceDisplay) {
                priceDisplay.textContent = `$${parseFloat(priceData.price).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
            }
        }
    }
}

function updateLastUpdateTime() {
    const timeElement = document.getElementById('last-update-time');
    if (timeElement && lastPriceUpdate) {
        const time = lastPriceUpdate.toLocaleTimeString();
        timeElement.textContent = `Last updated: ${time}`;
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

    // Load price predictions
    try {
        await updatePredictions();
    } catch (error) {
        console.error('Error loading price predictions:', error);
    }
}

// ============================================================================
// Data Collection
// ============================================================================

async function collectData() {
    try {
        // Get selected symbols from multi-select
        const symbolsSelect = document.getElementById('symbols-select');
        const symbols = Array.from(symbolsSelect.selectedOptions).map(o => o.value);

        // Get selected timeframes
        const timeframes = Array.from(document.getElementById('timeframes-select').selectedOptions).map(o => o.value);

        // Get limit
        const limit = parseInt(document.getElementById('limit-input').value);

        if (symbols.length === 0) {
            showNotification('Please select at least one symbol', 'error');
            return;
        }

        if (timeframes.length === 0) {
            showNotification('Please select at least one timeframe', 'error');
            return;
        }

        showNotification('Starting data collection...', 'info');

        const result = await apiCall('/data/collect', 'POST', {
            symbols,
            timeframes,
            limit
        });

        if (result && result.status === 'started') {
            showNotification(`Data collection started for ${symbols.join(', ')}`, 'success');
        } else {
            showNotification('Failed to start data collection', 'error');
        }
    } catch (error) {
        console.error('Error in collectData:', error);
        showNotification('Error starting data collection: ' + error.message, 'error');
    }
}

// ============================================================================
// Model Training
// ============================================================================

async function trainModels() {
    try {
        showNotification('Starting model training...', 'info');

        const result = await apiCall('/models/train?symbol=BTCUSDT', 'POST');

        if (result && result.status) {
            showNotification('Model training started successfully', 'success');

            // Update model status after a delay
            setTimeout(() => {
                loadModelStatus();
            }, 2000);
        } else {
            showNotification('Failed to start model training', 'error');
        }
    } catch (error) {
        console.error('Error in trainModels:', error);
        showNotification('Error starting model training: ' + error.message, 'error');
    }
}

async function loadModelStatus() {
    try {
        const result = await apiCall('/models/status');
        if (result) {
            // Update UI with model status
            const ltStatus = document.getElementById('lt-status');
            const stStatus = document.getElementById('st-status');
            const ltAccuracy = document.getElementById('lt-accuracy');
            const stAccuracy = document.getElementById('st-accuracy');

            if (ltStatus) ltStatus.textContent = result.long_term_status || 'Trained';
            if (stStatus) stStatus.textContent = result.short_term_status || 'Trained';
            if (ltAccuracy) ltAccuracy.textContent = (result.long_term_accuracy || 62) + '%';
            if (stAccuracy) stAccuracy.textContent = (result.short_term_accuracy || 58) + '%';
        }
    } catch (error) {
        console.error('Error loading model status:', error);
    }
}

// ============================================================================
// Backtesting
// ============================================================================

async function runBacktest() {
    try {
        const symbol = document.getElementById('backtest-symbol').value;
        const timeframe = document.getElementById('backtest-timeframe').value;
        const startDate = document.getElementById('backtest-start').value;
        const endDate = document.getElementById('backtest-end').value;
        const capital = parseFloat(document.getElementById('backtest-capital').value);

        // Validation
        if (!symbol) {
            showNotification('Please select a symbol', 'error');
            return;
        }
        if (!timeframe) {
            showNotification('Please select a timeframe', 'error');
            return;
        }
        if (!startDate) {
            showNotification('Please select a start date', 'error');
            return;
        }
        if (!endDate) {
            showNotification('Please select an end date', 'error');
            return;
        }
        if (isNaN(capital) || capital <= 0) {
            showNotification('Please enter a valid capital amount', 'error');
            return;
        }

        showNotification('Running backtest...', 'info');

        const result = await apiCall('/backtest/run', 'POST', {
            symbol,
            timeframe,
            start_date: startDate,
            end_date: endDate,
            initial_capital: capital
        });

        if (result && result.status) {
            showNotification('Backtest completed successfully', 'success');
            setTimeout(() => {
                loadBacktestResults();
            }, 1000);
        } else {
            showNotification('Failed to run backtest', 'error');
        }
    } catch (error) {
        console.error('Error in runBacktest:', error);
        showNotification('Error running backtest: ' + error.message, 'error');
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
    try {
        const mode = document.getElementById('trading-mode').value;

        if (!mode) {
            showNotification('Please select a trading mode', 'error');
            return;
        }

        // Validate mode
        const validModes = ['paper', 'testnet', 'live'];
        if (!validModes.includes(mode)) {
            showNotification('Invalid trading mode selected', 'error');
            return;
        }

        showNotification(`Starting trading in ${mode.toUpperCase()} mode...`, 'info');

        const result = await apiCall(`/trading/start?mode=${mode}`, 'POST');

        if (result && result.status === 'started') {
            const modeLabel = mode === 'paper' ? 'Paper Trading' :
                            mode === 'testnet' ? 'Testnet' : 'Live Trading';
            showNotification(
                `✓ Trading started successfully!\n` +
                `Mode: ${modeLabel}\n` +
                `Timestamp: ${new Date().toLocaleTimeString()}`,
                'success'
            );

            // Update UI to show trading is active
            const startBtn = document.querySelector('button[onclick="startTrading()"]');
            if (startBtn) {
                startBtn.disabled = true;
                startBtn.style.opacity = '0.5';
            }

            // Load positions after starting
            setTimeout(() => {
                loadTradingPositions();
            }, 500);
        } else {
            showNotification('Failed to start trading - no response from server', 'error');
        }
    } catch (error) {
        console.error('Error in startTrading:', error);
        showNotification('Error starting trading: ' + error.message, 'error');
    }
}

async function stopTrading() {
    try {
        showNotification('Stopping trading...', 'info');

        const result = await apiCall('/trading/stop', 'POST');

        if (result && result.status === 'stopped') {
            showNotification(
                `✓ Trading stopped successfully!\n` +
                `Timestamp: ${new Date().toLocaleTimeString()}`,
                'success'
            );

            // Update UI to show trading is inactive
            const startBtn = document.querySelector('button[onclick="startTrading()"]');
            if (startBtn) {
                startBtn.disabled = false;
                startBtn.style.opacity = '1';
            }
        } else {
            showNotification('Failed to stop trading - no response from server', 'error');
        }
    } catch (error) {
        console.error('Error in stopTrading:', error);
        showNotification('Error stopping trading: ' + error.message, 'error');
    }
}

async function placeOrder() {
    try {
        const symbol = document.getElementById('order-symbol').value;
        const side = document.getElementById('order-side').value;
        const size = parseFloat(document.getElementById('order-size').value);
        const leverage = parseFloat(document.getElementById('order-leverage').value);
        const mode = document.getElementById('trading-mode').value;

        // Comprehensive validation
        if (!symbol) {
            showNotification('Please select a symbol', 'error');
            return;
        }
        if (!side) {
            showNotification('Please select a side (long/short)', 'error');
            return;
        }
        if (isNaN(size) || size <= 0) {
            showNotification('Please enter a valid size (> 0)', 'error');
            return;
        }
        if (isNaN(leverage) || leverage < 1 || leverage > 125) {
            showNotification('Please enter a valid leverage (1-125x)', 'error');
            return;
        }

        showNotification(`Placing ${side} order for ${size} ${symbol} @ ${leverage}x leverage...`, 'info');

        const result = await apiCall('/trading/place-order', 'POST', {
            symbol,
            side,
            size,
            leverage,
            mode
        });

        if (result && result.status === 'success') {
            const entryPrice = result.entry_price || 'N/A';
            const liquidationPrice = result.liquidation_price || 'N/A';
            const orderId = result.order_id || 'N/A';

            showNotification(
                `✓ Order placed successfully!\n` +
                `Order ID: ${orderId}\n` +
                `Entry Price: $${entryPrice}\n` +
                `Liquidation: $${liquidationPrice}`,
                'success'
            );

            // Clear form
            document.getElementById('order-size').value = '1.0';
            document.getElementById('order-leverage').value = '1.0';

            // Reload positions after a short delay
            setTimeout(() => {
                loadTradingPositions();
            }, 500);
        } else if (result && result.status === 'error') {
            showNotification(`Order failed: ${result.message}`, 'error');
        } else {
            showNotification('Failed to place order - no response from server', 'error');
        }
    } catch (error) {
        console.error('Error in placeOrder:', error);
        showNotification('Error placing order: ' + error.message, 'error');
    }
}

async function loadTradingPositions() {
    try {
        const result = await apiCall('/trading/positions');
        if (result && result.positions !== undefined) {
            updatePositionsTable(result.positions);

            // Update account info if available
            if (result.total_positions !== undefined) {
                const posCountEl = document.getElementById('total-positions');
                if (posCountEl) {
                    posCountEl.textContent = result.total_positions;
                }
            }
        } else {
            console.warn('No positions data in response:', result);
        }
    } catch (error) {
        console.error('Error loading trading positions:', error);
    }
}

function updatePositionsTable(positions) {
    const tbody = document.getElementById('current-positions');
    if (!tbody) return;

    if (!positions || positions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: #999; padding: 20px;">No open positions</td></tr>';
        return;
    }

    tbody.innerHTML = positions.map(pos => {
        const pnlClass = pos.pnl >= 0 ? 'positive' : 'negative';
        const pnlSign = pos.pnl >= 0 ? '+' : '';
        const sideClass = pos.side === 'long' ? 'positive' : 'negative';

        return `
            <tr>
                <td><strong>${pos.symbol}</strong></td>
                <td><span class="${sideClass}">${pos.side.toUpperCase()}</span></td>
                <td>${pos.size}</td>
                <td>$${typeof pos.entry_price === 'number' ? pos.entry_price.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : pos.entry_price}</td>
                <td>$${typeof pos.current_price === 'number' ? pos.current_price.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : pos.current_price}</td>
                <td><strong class="${pnlClass}">$${pnlSign}${typeof pos.pnl === 'number' ? pos.pnl.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}) : pos.pnl}</strong></td>
                <td class="${pnlClass}"><strong>${pnlSign}${typeof pos.pnl_pct === 'number' ? pos.pnl_pct.toFixed(2) : pos.pnl_pct}%</strong></td>
                <td>${pos.leverage}x</td>
            </tr>
        `;
    }).join('');
}

// ============================================================================
// Risk Management
// ============================================================================

async function calculateRiskMetrics() {
    try {
        const entryPrice = parseFloat(document.getElementById('risk-entry-price').value);
        const currentPrice = parseFloat(document.getElementById('risk-current-price').value);
        const positionSize = parseFloat(document.getElementById('risk-position-size').value);
        const leverage = parseFloat(document.getElementById('risk-leverage').value);
        const fundingRate = parseFloat(document.getElementById('risk-funding-rate').value);

        // Validation
        if (isNaN(entryPrice) || entryPrice <= 0) {
            showNotification('Please enter a valid entry price', 'error');
            return;
        }
        if (isNaN(currentPrice) || currentPrice <= 0) {
            showNotification('Please enter a valid current price', 'error');
            return;
        }
        if (isNaN(positionSize) || positionSize <= 0) {
            showNotification('Please enter a valid position size', 'error');
            return;
        }
        if (isNaN(leverage) || leverage <= 0 || leverage > 125) {
            showNotification('Please enter a valid leverage (1-125x)', 'error');
            return;
        }
        if (isNaN(fundingRate)) {
            showNotification('Please enter a valid funding rate', 'error');
            return;
        }

        showNotification('Calculating risk metrics...', 'info');

        const result = await apiCall('/risk/metrics', 'POST', {
            entry_price: entryPrice,
            current_price: currentPrice,
            position_size_usd: positionSize,
            leverage,
            funding_rate: fundingRate,
            volatility: 0.25
        });

        if (result && result.liquidation_price !== undefined) {
            // Update liquidation price
            const liqPriceEl = document.getElementById('liq-price');
            if (liqPriceEl) {
                liqPriceEl.textContent = `$${result.liquidation_price.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
            }

            // Update liquidation distance
            const liqDistEl = document.getElementById('liq-distance');
            if (liqDistEl) {
                const distClass = result.liquidation_distance_pct > 20 ? 'positive' : (result.liquidation_distance_pct > 10 ? 'warning' : 'negative');
                liqDistEl.textContent = `${result.liquidation_distance_pct.toFixed(2)}%`;
                liqDistEl.className = distClass;
            }

            // Update max loss
            const maxLossUsdEl = document.getElementById('max-loss-usd');
            if (maxLossUsdEl) {
                maxLossUsdEl.textContent = `-$${result.max_loss_usd.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
                maxLossUsdEl.className = 'negative';
            }

            const maxLossPctEl = document.getElementById('max-loss-pct');
            if (maxLossPctEl) {
                maxLossPctEl.textContent = `-${result.max_loss_pct.toFixed(2)}%`;
                maxLossPctEl.className = 'negative';
            }

            // Update funding costs
            const fundingHourlyEl = document.getElementById('funding-hourly');
            if (fundingHourlyEl) {
                fundingHourlyEl.textContent = `$${result.funding_cost_hourly.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
            }

            const fundingDailyEl = document.getElementById('funding-daily');
            if (fundingDailyEl) {
                fundingDailyEl.textContent = `$${result.funding_cost_daily.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
            }

            showNotification('Risk metrics calculated successfully', 'success');
        } else {
            showNotification('Failed to calculate risk metrics', 'error');
        }
    } catch (error) {
        console.error('Error in calculateRiskMetrics:', error);
        showNotification('Error calculating risk metrics: ' + error.message, 'error');
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
// Price Predictions
// ============================================================================

async function updatePredictions() {
    try {
        const symbol = document.getElementById('predictions-coin-select').value;

        // Update current price immediately from real-time data
        updatePredictionsPrices();

        // Load long-term predictions
        const ltResponse = await apiCall(`/predictions/long-term?symbol=${symbol}`);
        if (ltResponse && ltResponse.predictions) {
            updateLongTermPredictions(ltResponse);
        }

        // Load short-term predictions
        const stResponse = await apiCall(`/predictions/short-term?symbol=${symbol}`);
        if (stResponse && stResponse.predictions) {
            updateShortTermPredictions(stResponse);
        }

        // Load chart data
        const ltChartData = await apiCall(`/predictions/chart-data/long-term?symbol=${symbol}`);
        if (ltChartData) {
            initializeLongTermPredictionsChart(ltChartData);
        }

        const stChartData = await apiCall(`/predictions/chart-data/short-term?symbol=${symbol}`);
        if (stChartData) {
            initializeShortTermPredictionsChart(stChartData);
        }
    } catch (error) {
        console.error('Error updating predictions:', error);
    }
}

function updateLongTermPredictions(data) {
    try {
        // Update current price
        const priceEl = document.getElementById('pred-current-price');
        if (priceEl) {
            priceEl.textContent = `$${data.current_price.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        }

        // Update last updated time
        const timeEl = document.getElementById('pred-last-updated');
        if (timeEl) {
            timeEl.textContent = 'Just now';
        }

        // Update summary
        if (data.predictions && data.predictions.length > 0) {
            const pred12m = data.predictions.find(p => p.timeframe_months === 12);
            if (pred12m) {
                const trendEl = document.getElementById('pred-long-trend');
                const confEl = document.getElementById('pred-long-confidence');
                if (trendEl) trendEl.textContent = pred12m.trend.toUpperCase();
                if (confEl) confEl.textContent = `${(pred12m.confidence * 100).toFixed(0)}%`;
            }
        }

        // Update table
        const tableBody = document.getElementById('long-term-predictions-table');
        if (tableBody && data.predictions) {
            tableBody.innerHTML = data.predictions.map(pred => `
                <tr>
                    <td>${pred.timeframe_months} Months</td>
                    <td>$${pred.predicted_price.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                    <td class="${pred.price_change_pct >= 0 ? 'positive' : 'negative'}">
                        ${pred.price_change_pct >= 0 ? '+' : ''}${pred.price_change_pct.toFixed(2)}%
                    </td>
                    <td>${(pred.confidence * 100).toFixed(0)}%</td>
                    <td><span class="badge ${pred.trend === 'up' ? 'up' : 'down'}">${pred.trend.toUpperCase()}</span></td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error updating long-term predictions:', error);
    }
}

function updateShortTermPredictions(data) {
    try {
        // Update summary
        if (data.predictions && data.predictions.length > 0) {
            const pred1d = data.predictions.find(p => p.timeframe === '1D');
            if (pred1d) {
                const trendEl = document.getElementById('pred-short-trend');
                const confEl = document.getElementById('pred-short-confidence');
                if (trendEl) trendEl.textContent = pred1d.signal.toUpperCase();
                if (confEl) confEl.textContent = `${(pred1d.confidence * 100).toFixed(0)}%`;
            }
        }

        // Update table
        const tableBody = document.getElementById('short-term-predictions-table');
        if (tableBody && data.predictions) {
            tableBody.innerHTML = data.predictions.map(pred => `
                <tr>
                    <td>${pred.timeframe}</td>
                    <td>$${pred.predicted_price.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                    <td class="${pred.price_change_pct >= 0 ? 'positive' : 'negative'}">
                        ${pred.price_change_pct >= 0 ? '+' : ''}${pred.price_change_pct.toFixed(2)}%
                    </td>
                    <td>${(pred.confidence * 100).toFixed(0)}%</td>
                    <td><span class="badge ${pred.signal === 'buy' ? 'buy' : (pred.signal === 'sell' ? 'sell' : 'hold')}">${pred.signal.toUpperCase()}</span></td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error updating short-term predictions:', error);
    }
}

function initializeLongTermPredictionsChart(data) {
    const ctx = document.getElementById('long-term-predictions-chart');
    if (!ctx) return;

    if (longTermPredictionsChart) {
        longTermPredictionsChart.destroy();
    }

    longTermPredictionsChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Predicted Price',
                    data: data.prices,
                    borderColor: chartColors.primary,
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointBackgroundColor: chartColors.primary,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                },
                {
                    label: 'Upper Confidence',
                    data: data.confidence_upper,
                    borderColor: 'rgba(52, 152, 219, 0.3)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                },
                {
                    label: 'Lower Confidence',
                    data: data.confidence_lower,
                    borderColor: 'rgba(52, 152, 219, 0.3)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: { color: '#666666', font: { size: 12 } }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: { color: '#e0e0e0' },
                    ticks: { color: '#666666' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#666666' }
                }
            }
        }
    });
}

function initializeShortTermPredictionsChart(data) {
    const ctx = document.getElementById('short-term-predictions-chart');
    if (!ctx) return;

    if (shortTermPredictionsChart) {
        shortTermPredictionsChart.destroy();
    }

    shortTermPredictionsChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'Predicted Price',
                    data: data.prices,
                    borderColor: chartColors.success,
                    backgroundColor: 'rgba(39, 174, 96, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 3,
                    pointBackgroundColor: chartColors.success,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 1
                },
                {
                    label: 'Upper Confidence',
                    data: data.confidence_upper,
                    borderColor: 'rgba(39, 174, 96, 0.3)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                },
                {
                    label: 'Lower Confidence',
                    data: data.confidence_lower,
                    borderColor: 'rgba(39, 174, 96, 0.3)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: { color: '#666666', font: { size: 12 } }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: { color: '#e0e0e0' },
                    ticks: { color: '#666666' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#666666' }
                }
            }
        }
    });
}

// ============================================================================
// Long-term Predictions Filter
// ============================================================================

async function updateLongTermChart() {
    try {
        const symbol = document.getElementById('predictions-coin-select').value;
        const timeframeFilter = document.getElementById('lt-timeframe-filter').value;

        const chartData = await apiCall(`/predictions/chart-data/long-term?symbol=${symbol}`);
        if (chartData) {
            initializeLongTermPredictionsChartFiltered(chartData, timeframeFilter);
        }
    } catch (error) {
        console.error('Error updating long-term chart:', error);
    }
}

function initializeLongTermPredictionsChartFiltered(data, timeframeFilter) {
    const ctx = document.getElementById('long-term-predictions-chart');
    if (!ctx) return;

    let labels = data.labels;
    let prices = data.prices;
    let upperBound = data.confidence_upper;
    let lowerBound = data.confidence_lower;

    // Filter data based on selected timeframe
    if (timeframeFilter !== 'all') {
        const maxMonths = parseInt(timeframeFilter);
        const timeframeMonths = [3, 6, 9, 12, 24, 36];
        const filterIndex = timeframeMonths.indexOf(maxMonths);

        if (filterIndex >= 0) {
            labels = labels.slice(0, filterIndex + 1);
            prices = prices.slice(0, filterIndex + 1);
            upperBound = upperBound.slice(0, filterIndex + 1);
            lowerBound = lowerBound.slice(0, filterIndex + 1);
        }
    }

    if (longTermPredictionsChart) {
        longTermPredictionsChart.destroy();
    }

    longTermPredictionsChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Predicted Price',
                    data: prices,
                    borderColor: chartColors.primary,
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointBackgroundColor: chartColors.primary,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                },
                {
                    label: 'Upper Confidence',
                    data: upperBound,
                    borderColor: 'rgba(52, 152, 219, 0.3)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                },
                {
                    label: 'Lower Confidence',
                    data: lowerBound,
                    borderColor: 'rgba(52, 152, 219, 0.3)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    fill: false,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: { color: '#666666', font: { size: 12 } }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: { color: '#e0e0e0' },
                    ticks: { color: '#666666' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#666666' }
                }
            }
        }
    });
}

// ============================================================================
// Paper Trading Simulation
// ============================================================================

let paperTradingData = {
    initialBalance: 100000,
    balance: 100000,
    positions: [],
    history: [],
    portfolioHistory: [100000]
};

function resetPaperTrading() {
    try {
        paperTradingData = {
            initialBalance: 100000,
            balance: 100000,
            positions: [],
            history: [],
            portfolioHistory: [100000]
        };
        updatePaperTradingUI();
        showNotification('Paper trading account reset successfully', 'success');
    } catch (error) {
        console.error('Error resetting paper trading:', error);
        showNotification('Error resetting account: ' + error.message, 'error');
    }
}

async function executePaperTrade() {
    try {
        const symbol = document.getElementById('paper-symbol').value;
        const tradeType = document.getElementById('paper-trade-type').value;
        const amount = parseFloat(document.getElementById('paper-amount').value);
        const leverage = parseFloat(document.getElementById('paper-leverage').value);

        // Validation
        if (!symbol) {
            showNotification('Please select a symbol', 'error');
            return;
        }
        if (!tradeType) {
            showNotification('Please select a trade type (long/short)', 'error');
            return;
        }
        if (isNaN(amount) || amount <= 0) {
            showNotification('Please enter a valid amount', 'error');
            return;
        }
        if (isNaN(leverage) || leverage <= 0) {
            showNotification('Please enter a valid leverage', 'error');
            return;
        }

        if (amount > paperTradingData.balance) {
            showNotification(`Insufficient balance. Available: $${paperTradingData.balance.toFixed(2)}`, 'error');
            return;
        }

        // Get current price from real-time data
        const priceData = currentPrices[symbol];
        if (!priceData || !priceData.price) {
            showNotification(`No price data available for ${symbol}. Please wait for price update.`, 'error');
            return;
        }

        const currentPrice = parseFloat(priceData.price);

        // Create position
        const position = {
            id: Date.now(),
            symbol: symbol,
            type: tradeType,
            entryPrice: currentPrice,
            currentPrice: currentPrice,
            amount: amount,
            leverage: leverage,
            entryTime: new Date().toLocaleString(),
            pnl: 0,
            pnlPct: 0
        };

        paperTradingData.positions.push(position);
        paperTradingData.balance -= amount;

        updatePaperTradingUI();
        showNotification(`${tradeType.toUpperCase()} position opened: ${symbol} @ $${currentPrice.toFixed(2)}`, 'success');
    } catch (error) {
        console.error('Error executing paper trade:', error);
        showNotification('Error executing trade: ' + error.message, 'error');
    }
}

function closePaperPosition(positionId) {
    const positionIndex = paperTradingData.positions.findIndex(p => p.id === positionId);
    if (positionIndex >= 0) {
        const position = paperTradingData.positions[positionIndex];

        // Calculate P&L
        const pnl = position.type === 'long'
            ? (position.currentPrice - position.entryPrice) * (position.amount / position.entryPrice)
            : (position.entryPrice - position.currentPrice) * (position.amount / position.entryPrice);

        const pnlPct = (pnl / position.amount) * 100;

        // Add to history
        paperTradingData.history.push({
            ...position,
            exitPrice: position.currentPrice,
            exitTime: new Date().toLocaleString(),
            pnl: pnl,
            pnlPct: pnlPct
        });

        // Update balance
        paperTradingData.balance += position.amount + pnl;

        // Remove from positions
        paperTradingData.positions.splice(positionIndex, 1);

        updatePaperTradingUI();
        showNotification(`Position closed: ${position.symbol}`, 'success');
    }
}

function updatePaperTradingUI() {
    // Update account metrics
    const portfolioValue = paperTradingData.balance +
        paperTradingData.positions.reduce((sum, p) => sum + p.amount, 0);
    const totalPnL = portfolioValue - paperTradingData.initialBalance;
    const returnPct = (totalPnL / paperTradingData.initialBalance) * 100;

    document.getElementById('paper-balance').textContent =
        `$${paperTradingData.balance.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
    document.getElementById('paper-portfolio-value').textContent =
        `$${portfolioValue.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
    document.getElementById('paper-total-pnl').textContent =
        `$${totalPnL.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
    document.getElementById('paper-return-pct').textContent =
        `${returnPct.toFixed(2)}%`;

    // Update positions table
    const positionsTable = document.getElementById('paper-positions-table');
    if (paperTradingData.positions.length === 0) {
        positionsTable.innerHTML = '<tr><td colspan="8" style="text-align: center; color: #999;">No open positions</td></tr>';
    } else {
        positionsTable.innerHTML = paperTradingData.positions.map(pos => `
            <tr>
                <td>${pos.symbol}</td>
                <td><span class="badge ${pos.type === 'long' ? 'buy' : 'sell'}">${pos.type.toUpperCase()}</span></td>
                <td>$${pos.entryPrice.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                <td>$${pos.currentPrice.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                <td>$${pos.amount.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                <td class="${pos.pnl >= 0 ? 'positive' : 'negative'}">$${pos.pnl.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                <td class="${pos.pnlPct >= 0 ? 'positive' : 'negative'}">${pos.pnlPct.toFixed(2)}%</td>
                <td><button class="btn btn-sm btn-danger" onclick="closePaperPosition(${pos.id})">Close</button></td>
            </tr>
        `).join('');
    }

    // Update history table
    const historyTable = document.getElementById('paper-history-table');
    if (paperTradingData.history.length === 0) {
        historyTable.innerHTML = '<tr><td colspan="8" style="text-align: center; color: #999;">No trade history</td></tr>';
    } else {
        historyTable.innerHTML = paperTradingData.history.map(trade => `
            <tr>
                <td>${trade.entryTime}</td>
                <td>${trade.symbol}</td>
                <td><span class="badge ${trade.type === 'long' ? 'buy' : 'sell'}">${trade.type.toUpperCase()}</span></td>
                <td>$${trade.entryPrice.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                <td>$${trade.exitPrice.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                <td>$${trade.amount.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                <td class="${trade.pnl >= 0 ? 'positive' : 'negative'}">$${trade.pnl.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                <td class="${trade.pnlPct >= 0 ? 'positive' : 'negative'}">${trade.pnlPct.toFixed(2)}%</td>
            </tr>
        `).join('');
    }

    // Update portfolio chart
    paperTradingData.portfolioHistory.push(portfolioValue);
    initializePaperPortfolioChart();
}

let paperPortfolioChart = null;

function initializePaperPortfolioChart() {
    const ctx = document.getElementById('paper-portfolio-chart');
    if (!ctx) return;

    if (paperPortfolioChart) {
        paperPortfolioChart.destroy();
    }

    paperPortfolioChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: Array.from({length: paperTradingData.portfolioHistory.length}, (_, i) => `Trade ${i}`),
            datasets: [{
                label: 'Portfolio Value',
                data: paperTradingData.portfolioHistory,
                borderColor: chartColors.primary,
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 3,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: { color: '#e0e0e0' },
                    ticks: { color: '#666666' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#666666' }
                }
            }
        }
    });
}

// ============================================================================
// Utilities
// ============================================================================

function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // Could be enhanced with a toast notification library
}

