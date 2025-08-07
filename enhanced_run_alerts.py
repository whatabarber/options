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
        # Save alerts to JSON file for dashboard
        with open('dashboard_data.json', 'w') as f:
            json.dump({
                'alerts': top_alerts,
                'last_updated': datetime.now().isoformat(),
                'total': len(all_alerts)
            }, f, indent=2)
        print("Saved alerts to dashboard_data.json")
        
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