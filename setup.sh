#!/bin/bash

echo "🚀 Setting up Enhanced Options Dashboard..."

# Create project directory structure
mkdir -p pages/api
mkdir -p styles
mkdir -p public

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies  
echo "📦 Installing Node.js dependencies..."
npm install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating .env file..."
    cp .env.template .env
    echo "⚠️  Please edit .env file with your actual tokens and URLs"
fi

# Initialize git if not already done
if [ ! -d .git ]; then
    echo "📝 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - Enhanced Options Dashboard"
fi

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your tokens"
echo "2. Run: python api_server.py (in one terminal)"
echo "3. Run: npm run dev (in another terminal)"
echo "4. Deploy to Vercel: vercel --prod"