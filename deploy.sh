#!/bin/bash
echo "🚀 Preparing Field Reader for Deployment..."

# 1. Check requirements
echo "📦 Verifying requirements..."
pip freeze > requirements_freeze.txt
# We stick to our manual requirements.txt to avoid clutter, but good to check.

# 2. Build Docker Image (Local Test)
echo "🐳 Building Docker Image..."
docker build -t field-reader-bot .

# 3. Instructions
echo ""
echo "✅ BUILD COMPLETE."
echo "To run locally in Docker:"
echo "  docker run -d --env-file .env field-reader-bot"
echo ""
echo "To deploy to Vercel (if using Python Runtime):"
echo "  vercel --prod"
echo ""
echo "To deploy to VPS:"
echo "  1. Copy this folder to VPS."
echo "  2. Run: docker-compose up -d --build"
echo ""
