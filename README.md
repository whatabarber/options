# 🎯 Enhanced Options Trading Dashboard

An AI-powered options flow dashboard with real-time alerts, Greeks analysis, and automated Discord notifications.

## ✨ Features

- **Real-time Options Scanning**: Monitors multiple tickers for high-probability setups
- **Advanced Filtering**: 2+ week expiration focus with customizable criteria  
- **Greeks Analysis**: Delta, Gamma, Theta, Vega calculations for risk assessment
- **AI-Powered Scoring**: Enhanced algorithm identifies most profitable opportunities
- **Live Dashboard**: Beautiful web interface with advanced filtering and sorting
- **Smart Discord Alerts**: Simplified notifications with dashboard link
- **Auto-GitHub Updates**: Automatic repository updates with scan results
- **Sweep Detection**: Identifies potential sweep-like activity

## 🚀 Quick Setup

1. **Clone and Setup**:
   ```bash
   git clone https://github.com/whatabarber/options.git
   cd options
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Configure Environment**:
   ```bash
   cp .env.template .env
   # Edit .env with your Discord webhook, GitHub tokens, etc.
   ```

3. **Start the System**:
   ```bash
   # Terminal 1: Start API server
   python api_server.py
   
   # Terminal 2: Start dashboard
   npm run dev
   ```

4. **Run Scanner**:
   ```bash
   python enhanced_run_alerts.py
   ```

## 📊 Dashboard Access

- **Local Development**: http://localhost:3000
- **API Endpoint**: http://localhost:5000

## 🔧 Configuration

### Environment Variables (.env)

```