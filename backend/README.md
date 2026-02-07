# Backend Setup Guide

## Quick Start with Docker

1. **Copy environment file**
   ```bash
   cd devops/docker
   cp .env.example .env
   # Edit .env and add your NCBI_EMAIL
   ```

2. **Start services**
   ```bash
   docker-compose up -d
   ```

3. **Check status**
   ```bash
   docker-compose ps
   ```

4. **View logs**
   ```bash
   docker-compose logs -f backend
   ```

5. **Access API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Health: http://localhost:8000/health

## Local Development Setup

1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run database (Docker)**
   ```bash
   docker run -d --name genomics_postgres \
     -e POSTGRES_DB=genomics_db \
     -e POSTGRES_USER=genomics_user \
     -e POSTGRES_PASSWORD=genomics_pass \
     -p 5432:5432 \
     postgres:15-alpine
   
   docker run -d --name genomics_redis \
     -p 6379:6379 \
     redis:7-alpine
   ```

5. **Run application**
   ```bash
   uvicorn app.main:app --reload
   ```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   └── core/
│       ├── config.py        # Settings
│       ├── logging.py       # Logging setup
│       ├── security.py      # CORS & rate limiting
│       └── exceptions.py    # Custom exceptions
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── Dockerfile              # Docker image
└── .env.example            # Environment template
```

## Environment Variables

Required:
- `NCBI_EMAIL`: Your email for NCBI API (required by NCBI)

Optional:
- `NCBI_API_KEY`: NCBI API key (increases rate limit)
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `DEBUG`: Enable debug mode (default: True)
- `LOG_LEVEL`: Logging level (default: INFO)

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/unit/test_config.py -v
```

## Next Steps

1. ✅ Backend foundation setup
2. ⏳ Database models (Phase 2)
3. ⏳ Analysis services (Phase 3)
4. ⏳ API endpoints (Phase 4)
