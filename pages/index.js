import { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Filter, AlertCircle, BarChart3, DollarSign, Clock, RefreshCw } from 'lucide-react';

export default function OptionsDashboard() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({
    total_alerts: 47,
    call_alerts: 29,
    put_alerts: 18,
    sweep_alerts: 12
  });

  useEffect(() => {
    // Demo data for now
    const demoAlerts = [
      {
        id: 1,
        ticker: 'TSLA',
        type: 'CALL',
        strike: 320,
        currentPrice: 309.50,
        expiration: '2025-08-22',
        daysToExpiration: 16,
        volume: 15420,
        openInterest: 8500,
        lastPrice: 12.50,
        score: 87.5,
        sweep: true,
        commentary: 'HIGH CONFIDENCE - Strong volume surge'
      },
      {
        id: 2,
        ticker: 'SPY',
        type: 'PUT',
        strike: 620,
        currentPrice: 628.50,
        expiration: '2025-08-29',
        daysToExpiration: 23,
        volume: 8750,
        openInterest: 12400,
        lastPrice: 8.75,
        score: 72.3,
        sweep: false,
        commentary: 'GOOD SETUP - Defensive positioning'
      }
    ];
    setAlerts(demoAlerts);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">🎯 Options Flow Dashboard</h1>
          <p className="text-gray-600">AI-powered options screening with enhanced analysis</p>
          
          <div className="mt-4 grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-blue-50 p-3 rounded-lg">
              <div className="flex items-center">
                <AlertCircle className="h-5 w-5 text-blue-600 mr-2" />
                <span className="text-sm font-medium text-blue-900">Total Alerts</span>
              </div>
              <div className="text-2xl font-bold text-blue-900">{stats.total_alerts}</div>
            </div>
            <div className="bg-green-50 p-3 rounded-lg">
              <div className="flex items-center">
                <TrendingUp className="h-5 w-5 text-green-600 mr-2" />
                <span className="text-sm font-medium text-green-900">Calls</span>
              </div>
              <div className="text-2xl font-bold text-green-900">{stats.call_alerts}</div>
            </div>
            <div className="bg-red-50 p-3 rounded-lg">
              <div className="flex items-center">
                <TrendingDown className="h-5 w-5 text-red-600 mr-2" />
                <span className="text-sm font-medium text-red-900">Puts</span>
              </div>
              <div className="text-2xl font-bold text-red-900">{stats.put_alerts}</div>
            </div>
            <div className="bg-purple-50 p-3 rounded-lg">
              <div className="flex items-center">
                <BarChart3 className="h-5 w-5 text-purple-600 mr-2" />
                <span className="text-sm font-medium text-purple-900">Sweeps</span>
              </div>
              <div className="text-2xl font-bold text-purple-900">{stats.sweep_alerts}</div>
            </div>
          </div>
        </div>

        {/* Alerts Table */}
        <div className="bg-white rounded-lg shadow-sm overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">High-Probability Options ({alerts.length} alerts)</h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Option</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Price</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Volume</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Score</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Analysis</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {alerts.map((alert) => (
                  <tr key={alert.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          alert.type === 'CALL' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {alert.type}
                        </span>
                        {alert.sweep && (
                          <span className="ml-2 inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-orange-100 text-orange-800">
                            🔥 SWEEP
                          </span>
                        )}
                      </div>
                      <div className="mt-1">
                        <div className="text-sm font-medium text-gray-900">{alert.ticker}</div>
                        <div className="text-sm text-gray-500">${alert.strike} | {alert.expiration}</div>
                        <div className="text-xs text-gray-500">{alert.daysToExpiration} days</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium">${alert.lastPrice}</div>
                      <div className="text-xs text-gray-500">Stock: ${alert.currentPrice}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm">{alert.volume?.toLocaleString()}</div>
                      <div className="text-xs text-gray-500">OI: {alert.openInterest?.toLocaleString()}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`text-lg font-bold ${
                        alert.score >= 80 ? 'text-green-600' : alert.score >= 65 ? 'text-blue-600' : 'text-yellow-600'
                      }`}>
                        {alert.score}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-xs text-gray-600 max-w-xs">{alert.commentary}</div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="mt-6 text-center text-gray-500">
          <p>🚀 Dashboard is live! Run your Python scanner to populate with real data.</p>
        </div>
      </div>
    </div>
  );
}