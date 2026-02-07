#!/bin/bash

# Quick start script for development environment

echo "🧬 Genomic Analysis Platform - Quick Start"
echo "=========================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Navigate to docker directory
cd "$(dirname "$0")/../devops/docker" || exit

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit devops/docker/.env and add your NCBI_EMAIL before continuing."
    echo "   Then run this script again."
    exit 0
fi

echo "✅ Environment file found"

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Access points:"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Health Check: http://localhost:8000/health"
echo ""
echo "📝 Useful commands:"
echo "   - View logs: docker-compose logs -f backend"
echo "   - Stop services: docker-compose down"
echo "   - Restart: docker-compose restart"
echo ""
