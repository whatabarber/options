import { useState, useEffect } from 'react';
import axios from 'axios';
import { Calendar, TrendingUp, TrendingDown, Filter, AlertCircle, BarChart3, DollarSign, Clock, RefreshCw } from 'lucide-react';

export default function OptionsDashboard() {
  const [alerts, setAlerts] = useState([]);
  const [filteredAlerts, setFilteredAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [stats, setStats] = useState({});
  const [filters, setFilters] = useState({
    minExpiration: 14,
    maxExpiration: 60,
    minVolume: 100,
    minOpenInterest: 500,
    minScore: 50,
    tickerFilter: '',
    optionType: 'all'
  });
  const [sortBy, setSortBy] = useState('score');
  const [sortOrder, setSortOrder] = useState('desc');

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/alerts');
      setAlerts(response.data.alerts || []);
      setLastUpdated(response.data.last_updated);
      
      // Fetch stats
      const statsResponse = await axios.get('/api/stats');
      setStats(statsResponse.data);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
    // Set up auto-refresh every 30 seconds
    const interval = setInterval(fetchAlerts, 30000);
    return () => clearInterval(interval);
  }, []);

  // Filter and sort alerts
  useEffect(() => {
    let filtered = alerts.filter(alert => {
      return (
        alert.daysToExpiration >= filters.minExpiration &&
        alert.daysToExpiration <= filters.maxExpiration &&
        alert.volume >= filters.minVolume &&
        alert.openInterest >= filters.minOpenInterest &&
        alert.score >= filters.minScore &&
        (filters.tickerFilter === '' || alert.ticker.toLowerCase().includes(filters.tickerFilter.toLowerCase())) &&
        (filters.optionType === 'all' || alert.type.toLowerCase() === filters.optionType.toLowerCase())
      );
    });

    filtered.sort((a, b) => {
      const multiplier = sortOrder === 'desc' ? -1 : 1;
      if (sortBy === 'score') return multiplier * (a.score - b.score);
      if (sortBy === 'volume') return multiplier * (a.volume - b.volume);
      if (sortBy === 'expiration') return multiplier * (a.daysToExpiration - b.daysToExpiration);
      if (sortBy === 'iv') return multiplier * (a.impliedVolatility - b.impliedVolatility);
      return 0;
    });

    setFilteredAlerts(filtered);
  }, [alerts, filters, sortBy, sortOrder]);

  const getMoneyness = (strike, currentPrice, type) => {
    const diff = type === 'CALL' ? (currentPrice - strike) : (strike - currentPrice);
    const percentage = (diff / currentPrice) * 100;
    if (Math.abs(percentage) < 2) return { label: 'ATM', color: 'text-yellow-600' };
    if (percentage > 0) return { label: 'ITM', color: 'text-green-600' };
    return { label: 'OTM', color: 'text-red-600' };
  };

  const formatCurrency = (value) => `${value?.toFixed(2) || '0.00'}`;
  const formatPercentage = (value) => `${((value || 0) * 100).toFixed(1)}%`;

  const getConfidenceColor = (score) => {
    if (score >= 80) return 'text-green-600 font-bold';
    if (score >= 65) return 'text-blue-600 font-semibold';
    if (score >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getConfidenceEmoji = (score) => {
    if (score >= 80) return '🎯';
    if (score >= 65) return '✅';
    if (score >= 50) return '⚠️';
    return '❌';
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Live Options Flow Dashboard</h1>
              <p className="text-gray-600">AI-powered options screening with Greeks analysis</p>
            </div>
            <button 
              onClick={fetchAlerts}
              disabled={loading}
              className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
              {loading ? 'Updating...' : 'Refresh'}
            </button>
          </div>
          
          <div className="mt-4 grid grid-cols-1 md:grid-cols-5 gap-4">
            <div className="bg-blue-50 p-3 rounded-lg">
              <div className="flex items-center">
                <AlertCircle className="h-5 w-5 text-blue-600 mr-2" />
                <span className="text-sm font-medium text-blue-900">Total Alerts</span>
              </div>
              <div className="text-2xl font-bold text-blue-900">{stats.total_alerts || filteredAlerts.length}</div>
            </div>
            <div className="bg-green-50 p-3 rounded-lg">
              <div className="flex items-center">
                <TrendingUp className="h-5 w-5 text-green-600 mr-2" />
                <span className="text-sm font-medium text-green-900">Calls</span>
              </div>
              <div className="text-2xl font-bold text-green-900">
                {stats.call_alerts || filteredAlerts.filter(a => a.type === 'CALL').length}
              </div>
            </div>
            <div className="bg-red-50 p-3 rounded-lg">
              <div className="flex items-center">
                <TrendingDown className="h-5 w-5 text-red-600 mr-2" />
                <span className="text-sm font-medium text-red-900">Puts</span>
              </div>
              <div className="text-2xl font-bold text-red-900">
                {stats.put_alerts || filteredAlerts.filter(a => a.type === 'PUT').length}
              </div>
            </div>
            <div className="bg-purple-50 p-3 rounded-lg">
              <div className="flex items-center">
                <BarChart3 className="h-5 w-5 text-purple-600 mr-2" />
                <span className="text-sm font-medium text-purple-900">Sweeps</span>
              </div>
              <div className="text-2xl font-bold text-purple-900">
                {stats.sweep_alerts || filteredAlerts.filter(a => a.sweep).length}
              </div>
            </div>
            <div className="bg-orange-50 p-3 rounded-lg">
              <div className="flex items-center">
                <DollarSign className="h-5 w-5 text-orange-600 mr-2" />
                <span className="text-sm font-medium text-orange-900">High Confidence</span>
              </div>
              <div className="text-2xl font-bold text-orange-900">
                {filteredAlerts.filter(a => a.score >= 80).length}
              </div>
            </div>
          </div>
          
          {lastUpdated && (
            <div className="mt-4 text-sm text-gray-500">
              Last updated: {new Date(lastUpdated).toLocaleString()}
            </div>
          )}
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex items-center mb-4">
            <Filter className="h-5 w-5 text-gray-600 mr-2" />
            <h2 className="text-lg font-semibold text-gray-900">Advanced Filters</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Min Days to Expiration</label>
              <input
                type="number"
                value={filters.minExpiration}
                onChange={(e) => setFilters({...filters, minExpiration: parseInt(e.target.value)})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Max Days to Expiration</label>
              <input
                type="number"
                value={filters.maxExpiration}
                onChange={(e) => setFilters({...filters, maxExpiration: parseInt(e.target.value)})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Min Volume</label>
              <input
                type="number"
                value={filters.minVolume}
                onChange={(e) => setFilters({...filters, minVolume: parseInt(e.target.value)})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Min Score</label>
              <input
                type="number"
                value={filters.minScore}
                onChange={(e) => setFilters({...filters, minScore: parseInt(e.target.value)})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Ticker Filter</label>
              <input
                type="text"
                value={filters.tickerFilter}
                onChange={(e) => setFilters({...filters, tickerFilter: e.target.value})}
                placeholder="Enter ticker..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Option Type</label>
              <select
                value={filters.optionType}
                onChange={(e) => setFilters({...filters, optionType: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All</option>
                <option value="call">Calls Only</option>
                <option value="put">Puts Only</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Sort By</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="score">Score</option>
                <option value="volume">Volume</option>
                <option value="expiration">Days to Expiration</option>
                <option value="iv">Implied Volatility</option>
              </select>
            </div>
          </div>
        </div>

        {/* Alerts Table */}
        <div className="bg-white rounded-lg shadow-sm overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">
              High-Probability Options ({filteredAlerts.length} alerts)
            </h2>
          </div>
          
          {loading ? (
            <div className="flex justify-center items-center py-12">
              <RefreshCw className="h-8 w-8 animate-spin text-blue-600" />
              <span className="ml-2 text-gray-600">Loading alerts...</span>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Option Details
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Pricing & Moneyness
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Volume & Flow
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Greeks & Risk
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      AI Analysis
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredAlerts.map((alert, index) => {
                    const moneyness = getMoneyness(alert.strike, alert.currentPrice, alert.type);
                    return (
                      <tr key={`${alert.ticker}-${alert.strike}-${alert.expiration}-${index}`} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="flex-shrink-0">
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
                          </div>
                          <div className="mt-1">
                            <div className="text-sm font-medium text-gray-900">{alert.ticker}</div>
                            <div className="text-sm text-gray-500">
                              ${alert.strike} | {alert.expiration}
                            </div>
                            <div className="flex items-center mt-1">
                              <Clock className="h-3 w-3 text-gray-400 mr-1" />
                              <span className="text-xs text-gray-500">{alert.daysToExpiration} days</span>
                              <span className={`ml-2 text-xs font-medium ${moneyness.color}`}>
                                {moneyness.label}
                              </span>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900">
                            <div className="font-medium">Premium: {formatCurrency(alert.lastPrice)}</div>
                            <div className="text-gray-500">Stock: {formatCurrency(alert.currentPrice)}</div>
                            <div className="text-gray-500">Strike: {formatCurrency(alert.strike)}</div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900">
                            <div className="font-medium">Vol: {alert.volume?.toLocaleString() || 'N/A'}</div>
                            <div className="text-gray-500">OI: {alert.openInterest?.toLocaleString() || 'N/A'}</div>
                            <div className="text-xs text-gray-400">
                              Ratio: {alert.volume && alert.openInterest ? (alert.volume / alert.openInterest).toFixed(2) : 'N/A'}
                            </div>
                            <div className="text-xs text-blue-600 mt-1">
                              IV: {formatPercentage(alert.impliedVolatility)}
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900">
                            {alert.delta !== undefined ? (
                              <>
                                <div className="text-xs">Δ: {alert.delta.toFixed(3)}</div>
                                <div className="text-xs">Γ: {alert.gamma?.toFixed(4) || 'N/A'}</div>
                                <div className="text-xs">Θ: {alert.theta?.toFixed(2) || 'N/A'}</div>
                                <div className="text-xs">ν: {alert.vega?.toFixed(3) || 'N/A'}</div>
                              </>
                            ) : (
                              <div className="text-xs text-gray-400">Greeks calculating...</div>
                            )}
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div className="text-sm text-gray-900">
                            <div className="flex items-center mb-2">
                              <span className="text-xs mr-1">{getConfidenceEmoji(alert.score)}</span>
                              <span className={`text-lg font-bold ${getConfidenceColor(alert.score)}`}>
                                {alert.score?.toFixed(0) || 'N/A'}
                              </span>
                              <span className="ml-1 text-xs text-gray-500">score</span>
                            </div>
                            <div className="text-xs text-gray-600 max-w-xs leading-relaxed">
                              {alert.commentary || 'Analysis pending...'}
                            </div>
                            <div className="text-xs text-gray-400 mt-2">
                              {alert.timestamp ? new Date(alert.timestamp).toLocaleTimeString() : 'Recently'}
                            </div>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {filteredAlerts.length === 0 && !loading && (
          <div className="text-center py-12">
            <div className="text-gray-500 text-lg">No alerts match your current filters</div>
            <div className="text-gray-400 text-sm mt-2">Try adjusting your filter criteria or refresh for new data</div>
          </div>
        )}
      </div>
    </div>
  );
}