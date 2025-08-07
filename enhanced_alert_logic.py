import yfinance as yf
import numpy as np
from py_vollib.black_scholes import black_scholes
from py_vollib.black_scholes.greeks.analytical import delta, gamma, theta, vega
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

def get_risk_free_rate():
    """Get current risk-free rate (10-year treasury)"""
    try:
        treasury = yf.Ticker("^TNX")
        rate = treasury.history(period="1d")["Close"].iloc[-1] / 100
        return rate if rate > 0 else 0.045  # Default to 4.5%
    except:
        return 0.045

def calculate_greeks(current_price, strike, time_to_expiry, risk_free_rate, implied_vol, option_type):
    """Calculate option Greeks"""
    try:
        if time_to_expiry <= 0 or implied_vol <= 0:
            return None
        
        flag = 'c' if option_type == 'CALL' else 'p'
        
        greeks = {
            'delta': delta(flag, current_price, strike, time_to_expiry, risk_free_rate, implied_vol),
            'gamma': gamma(flag, current_price, strike, time_to_expiry, risk_free_rate, implied_vol),
            'theta': theta(flag, current_price, strike, time_to_expiry, risk_free_rate, implied_vol),
            'vega': vega(flag, current_price, strike, time_to_expiry, risk_free_rate, implied_vol)
        }
        return greeks
    except:
        return None

def calculate_enhanced_score(alert, greeks):
    """Enhanced scoring algorithm with Greeks and profitability factors"""
    base_score = 0
    
    # Volume momentum (30% weight)
    volume_ratio = alert["volume"] / max(alert["openInterest"], 1)
    if volume_ratio > 3:
        base_score += 30
    elif volume_ratio > 2:
        base_score += 20
    elif volume_ratio > 1:
        base_score += 10
    
    # Implied Volatility analysis (25% weight)
    iv = alert["impliedVolatility"]
    if 0.3 <= iv <= 0.8:  # Sweet spot for IV
        base_score += 25
    elif 0.8 < iv <= 1.2:  # High but manageable
        base_score += 15
    elif iv > 1.2:  # Very high - risky
        base_score += 5
    
    # Moneyness analysis (20% weight)
    current_price = alert["currentPrice"]
    strike = alert["strike"]
    if alert["type"] == "CALL":
        moneyness = (current_price - strike) / current_price
    else:
        moneyness = (strike - current_price) / current_price
    
    if -0.05 <= moneyness <= 0.05:  # Near ATM
        base_score += 20
    elif -0.1 <= moneyness <= 0.1:  # Close to ATM
        base_score += 15
    elif moneyness > 0:  # ITM
        base_score += 10
    
    # Time decay consideration (15% weight)
    days_to_exp = alert["daysToExpiration"]
    if 21 <= days_to_exp <= 45:  # Sweet spot
        base_score += 15
    elif 14 <= days_to_exp <= 60:  # Acceptable range
        base_score += 10
    elif days_to_exp < 14:  # Too short
        base_score -= 10
    
    # Greeks bonus (10% weight)
    if greeks:
        if alert["type"] == "CALL":
            if 0.3 <= greeks["delta"] <= 0.7:  # Good delta range
                base_score += 5
            if greeks["theta"] > -1.0:  # Manageable time decay
                base_score += 3
        else:  # PUT
            if -0.7 <= greeks["delta"] <= -0.3:  # Good delta range
                base_score += 5
            if greeks["theta"] > -1.0:  # Manageable time decay
                base_score += 3
    
    return min(base_score, 100)  # Cap at 100

def scan_options_enhanced(ticker):
    """Enhanced options scanning with Greeks and better filtering"""
    from config import MIN_DAYS_TO_EXPIRATION, MAX_DAYS_TO_EXPIRATION
    
    stock = yf.Ticker(ticker)
    alerts = []
    risk_free_rate = get_risk_free_rate()
    
    try:
        # Get multiple expiration dates
        expirations = stock.options[:4]  # Get first 4 expirations instead of just 1
        current_price = stock.history(period="1d")["Close"].iloc[-1]
        
        for exp in expirations:
            exp_date = datetime.strptime(exp, "%Y-%m-%d")
            days_to_exp = (exp_date - datetime.now()).days
            
            # Filter by expiration range
            if days_to_exp < MIN_DAYS_TO_EXPIRATION or days_to_exp > MAX_DAYS_TO_EXPIRATION:
                continue
            
            time_to_expiry = days_to_exp / 365.0
            
            # Scan both calls and puts
            option_chain = stock.option_chain(exp)
            
            for option_type, options_df in [("CALL", option_chain.calls), ("PUT", option_chain.puts)]:
                for _, row in options_df.iterrows():
                    volume = row.get("volume", 0) or 0
                    oi = row.get("openInterest", 0) or 0
                    strike = row["strike"]
                    last_price = row.get("lastPrice", 0) or 0
                    iv = row.get("impliedVolatility", 0) or 0
                    
                    # Enhanced filtering criteria
                    if (volume >= 100 and oi >= 500 and 
                        abs(strike - current_price) / current_price <= 0.15 and  # Within 15% of current price
                        iv > 0.1 and iv < 3.0 and  # Reasonable IV range
                        last_price > 0.1):  # Minimum option price
                        
                        # Calculate Greeks
                        greeks = calculate_greeks(current_price, strike, time_to_expiry, 
                                                risk_free_rate, iv, option_type)
                        
                        alert = {
                            "ticker": ticker,
                            "type": option_type,
                            "strike": strike,
                            "currentPrice": current_price,
                            "expiration": exp,
                            "daysToExpiration": days_to_exp,
                            "volume": volume,
                            "openInterest": oi,
                            "lastPrice": last_price,
                            "impliedVolatility": iv,
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        # Add Greeks if calculated successfully
                        if greeks:
                            alert.update({
                                "delta": greeks["delta"],
                                "gamma": greeks["gamma"],
                                "theta": greeks["theta"],
                                "vega": greeks["vega"]
                            })
                        
                        # Enhanced scoring
                        alert["score"] = calculate_enhanced_score(alert, greeks)
                        
                        # Sweep detection
                        sweep_like = volume > 3 * oi if oi > 0 else False
                        alert["sweep"] = sweep_like
                        
                        alerts.append(alert)
                        
    except Exception as e:
        print(f"Error scanning {ticker}: {e}")
    
    return alerts