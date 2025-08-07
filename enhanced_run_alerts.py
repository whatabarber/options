import requests
import json
from datetime import datetime
from config import TICKERS, DISCORD_WEBHOOK, MAX_ALERTS, DASHBOARD_URL
from enhanced_alert_logic import scan_options_enhanced
from discord_alert_enhanced import send_dashboard_alert
from history_logger import log_alerts
from ai_commentary_enhanced import generate_enhanced_commentary
from github_updater import update_github_repo, setup_github_remote

def main():
    """Enhanced main function with API integration"""
    print(f"Starting enhanced options scan at {datetime.now()}")
    
    # Setup GitHub if tokens are provided
    setup_github_remote()
    
    all_alerts = []
    
    # Scan all tickers
    for ticker in TICKERS:
        print(f"Scanning {ticker}...")
        alerts = scan_options_enhanced(ticker)
        
        # Add enhanced commentary to each alert
        for alert in alerts:
            alert['commentary'] = generate_enhanced_commentary(alert)
        
        all_alerts.extend(alerts)
        print(f"Found {len(alerts)} alerts for {ticker}")
    
    # Sort by score and limit results
    all_alerts.sort(key=lambda x: x['score'], reverse=True)
    top_alerts = all_alerts[:MAX_ALERTS]
    
    print(f"Total alerts found: {len(all_alerts)}")
    print(f"Top alerts selected: {len(top_alerts)}")
    
    if top_alerts:
        # Send alerts to API server
        try:
            api_response = requests.post('http://localhost:5000/api/alerts', 
                                       json={'alerts': top_alerts},
                                       timeout=10)
            if api_response.status_code == 200:
                print("Successfully updated API server")
            else:
                print(f"API server update failed: {api_response.status_code}")
        except Exception as e:
            print(f"Could not reach API server: {e}")
        
        # Send simplified Discord alert with dashboard link
        send_dashboard_alert(len(all_alerts), top_alerts, DISCORD_WEBHOOK)
        
        # Log to CSV
        log_alerts(top_alerts)
        
        # Update GitHub repo
        update_github_repo()
        
        print(f"Process completed. Dashboard available at: {DASHBOARD_URL}")
    else:
        print("No alerts found matching criteria")

if __name__ == "__main__":
    main()