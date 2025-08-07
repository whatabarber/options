import os
from dotenv import load_dotenv

load_dotenv()

TICKERS = ["TSLA", "SPY", "PLTR", "DKS", "RBLX", "AAPL", "NVDA", "AMD", "QQQ", "IWM"]
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "https://discord.com/api/webhooks/1395083791890120754/AdAdVz3eHPQhi3i1iIORpKylHCpFokxsyUJeIvgo8Js1jtIZf30hp5BQk6XKYx_hemZa")
ENABLE_CHARTS = True
MAX_ALERTS = 50  # Increased for dashboard
MIN_DAYS_TO_EXPIRATION = 14  # At least 2 weeks
MAX_DAYS_TO_EXPIRATION = 60  # Maximum 2 months
DASHBOARD_URL = os.getenv("DASHBOARD_URL", "http://localhost:3000")

# GitHub settings
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "your_github_token_here")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "your_github_username_here")
GITHUB_REPO = "options"