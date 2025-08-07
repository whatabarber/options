import requests
from config import DASHBOARD_URL

def send_dashboard_alert(total_alerts, top_alerts, webhook):
    """Send simplified Discord alert with dashboard link"""
    
    # Create summary of top 3 alerts
    top_3_summary = []
    for i, alert in enumerate(top_alerts[:3], 1):
        confidence = "🎯" if alert['score'] >= 80 else "✅" if alert['score'] >= 65 else "⚠️"
        sweep_indicator = "🔥 SWEEP" if alert.get('sweep', False) else ""
        
        summary = f"{i}. {alert['ticker']} {alert['type']} ${alert['strike']} | Score: {alert['score']} {confidence} {sweep_indicator}"
        top_3_summary.append(summary)
    
    content = f"""
🚨 **OPTIONS DASHBOARD UPDATE** 🚨

📊 **{total_alerts} New High-Quality Alerts Found**

**🏆 TOP 3 OPPORTUNITIES:**
{chr(10).join(top_3_summary)}

🎯 **View Full Analysis & All Alerts:**
{DASHBOARD_URL}

⏰ Updated: {top_alerts[0]['timestamp'][:16] if top_alerts else 'Now'}
"""
    
    try:
        response = requests.post(webhook, data={"content": content})
        if response.status_code == 204:
            print("Dashboard alert sent successfully")
        else:
            print(f"Discord alert failed: {response.status_code}")
    except Exception as e:
        print(f"Error sending Discord alert: {e}")