# Deployment Guide

This guide describes how to deploy the Genomic Analysis Platform using Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- NCBI API Key (recommended)

## Configuration

1. **Environment Variables**
   
   Copy the example environment file:
   ```bash
   cd devops/docker
   cp .env.example .env
   ```

   Edit `.env` and configure:
   - `NCBI_EMAIL`: Your email (required by NCBI)
   - `NCBI_API_KEY`: Your NCBI API Key (optional but recommended)

## Deployment Steps

### 1. Build and Start Services

Run the following command to build images and start all services:

```bash
cd devops/docker
docker-compose up -d --build
```

This will start:
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **PostgreSQL**: Port 5432
- **Redis**: Port 6379
- **Celery Worker**: Background processing

### 2. Verify Deployment

Check the status of containers:

```bash
docker-compose ps
```

View logs:

```bash
docker-compose logs -f
```

### 3. Database Management

The database is automatically initialized. To reset it:

```bash
docker-compose down -v
docker-compose up -d
```

## Running Tests

To run backend tests *inside* the Docker container (ensuring consistent environment):

```bash
# Enter the backend container
docker-compose exec backend bash

# Run tests
pytest tests/
```

## Production Considerations

For a production deployment:

1.  **Security**:
    - Change `SECRET_KEY` in `backend/.env`
    - Change database passwords
    - Set `DEBUG=False`

2.  **Performance**:
    - Increase Celery workers if needed: `docker-compose up -d --scale celery_worker=3`
    - Configure Redis persistence

3.  **Logs**:
    - Logs are persisted in `logs/` directory

## Troubleshooting

- **Database Connection Failed**: Ensure PostgreSQL is healthy (`docker-compose ps`).
- **NCBI Rate Limited**: Add `NCBI_API_KEY` to `.env`.
- **Frontend API Errors**: Check `VITE_API_URL` in `frontend/.env`.
