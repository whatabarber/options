import yfinance as yf
from datetime import datetime

ticker = "SPY"
stock = yf.Ticker(ticker)
current_price = stock.history(period="1d")["Close"].iloc[-1]

print(f"Testing {ticker} - Current Price: ${current_price}")

expirations = stock.options[:2]
for exp in expirations:
    print(f"\nExpiration: {exp}")
    options = stock.option_chain(exp).calls
    print(f"Total call options: {len(options)}")
    
    count = 0
    for _, row in options.iterrows():
        if count >= 5:  # Only check first 5
            break
        volume = row.get("volume", 0) or 0
        oi = row.get("openInterest", 0) or 0
        iv = row.get("impliedVolatility", 0) or 0
        last_price = row.get("lastPrice", 0) or 0
        
        print(f"Strike: ${row['strike']}")
        print(f"  Volume: {volume}")
        print(f"  OI: {oi}")
        print(f"  IV: {iv}")
        print(f"  Last Price: ${last_price}")
        print(f"  Strike distance: {abs(row['strike'] - current_price)}")
        print()
        
        count += 1