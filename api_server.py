from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Global storage for alerts (in production, use a database)
alerts_data = []

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get all alerts with optional filtering"""
    try:
        # Parse query parameters for filtering
        ticker_filter = request.args.get('ticker', '').upper()
        option_type = request.args.get('type', 'all').upper()
        min_score = float(request.args.get('min_score', 0))
        min_expiration = int(request.args.get('min_expiration', 0))
        max_expiration = int(request.args.get('max_expiration', 365))
        
        filtered_alerts = alerts_data
        
        # Apply filters
        if ticker_filter:
            filtered_alerts = [a for a in filtered_alerts if ticker_filter in a.get('ticker', '')]
        
        if option_type != 'ALL':
            filtered_alerts = [a for a in filtered_alerts if a.get('type') == option_type]
        
        if min_score > 0:
            filtered_alerts = [a for a in filtered_alerts if a.get('score', 0) >= min_score]
        
        filtered_alerts = [a for a in filtered_alerts 
                          if min_expiration <= a.get('daysToExpiration', 0) <= max_expiration]
        
        # Sort by score descending
        filtered_alerts.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return jsonify({
            'alerts': filtered_alerts,
            'total': len(filtered_alerts),
            'last_updated': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts', methods=['POST'])
def update_alerts():
    """Update alerts data (called by Python bot)"""
    try:
        global alerts_data
        new_alerts = request.json.get('alerts', [])
        
        # Store the new alerts
        alerts_data = new_alerts
        
        # Save to file as backup
        with open('alerts_backup.json', 'w') as f:
            json.dump(alerts_data, f, indent=2)
        
        return jsonify({'status': 'success', 'count': len(alerts_data)})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    try:
        total_alerts = len(alerts_data)
        call_alerts = len([a for a in alerts_data if a.get('type') == 'CALL'])
        put_alerts = len([a for a in alerts_data if a.get('type') == 'PUT'])
        sweep_alerts = len([a for a in alerts_data if a.get('sweep', False)])
        
        return jsonify({
            'total_alerts': total_alerts,
            'call_alerts': call_alerts,
            'put_alerts': put_alerts,
            'sweep_alerts': sweep_alerts,
            'last_updated': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load existing alerts if backup exists
    if os.path.exists('alerts_backup.json'):
        try:
            with open('alerts_backup.json', 'r') as f:
                alerts_data = json.load(f)
            print(f"Loaded {len(alerts_data)} alerts from backup")
        except:
            alerts_data = []
    
    app.run(host='0.0.0.0', port=5000, debug=True)