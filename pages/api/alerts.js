export default async function handler(req, res) {
  const API_BASE_URL = process.env.PYTHON_API_URL || 'http://localhost:5000';
  
  if (req.method === 'GET') {
    try {
      const response = await fetch(`${API_BASE_URL}/api/alerts?${new URLSearchParams(req.query)}`);
      const data = await response.json();
      res.status(200).json(data);
    } catch (error) {
      console.error('Error fetching alerts:', error);
      res.status(500).json({ error: 'Failed to fetch alerts', alerts: [] });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}