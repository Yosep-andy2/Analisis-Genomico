# Celery Tasks Documentation

## Overview

The application uses Celery for asynchronous task processing. This allows long-running genome analysis to run in the background without blocking the API.

## Architecture

```
API Request → Create Analysis Record → Queue Celery Task → Return Task ID
                                              ↓
                                    Background Processing
                                              ↓
                                    Update Database with Results
```

## Tasks

### Download Task

**Task**: `download_genome`  
**Queue**: `downloads`  
**Purpose**: Download genome from NCBI

```python
from app.tasks.download_tasks import download_genome_task

result = download_genome_task.delay("NC_000913.3")
```

### Analysis Task

**Task**: `analyze_genome`  
**Queue**: `analysis`  
**Purpose**: Complete genome analysis pipeline

**Steps**:
1. Codon analysis (10% progress)
2. Gene analysis (35% progress)
3. Genome statistics (60% progress)
4. Validation (80% progress)
5. Visualization (90% progress)
6. Complete (100% progress)

```python
from app.tasks.analysis_tasks import analyze_genome_task

result = analyze_genome_task.delay(
    analysis_id=1,
    genbank_file="/path/to/genome.gb",
    accession="NC_000913.3"
)
```

## Running Celery Worker

### Development

```bash
# Single worker
celery -A app.tasks.celery_app worker --loglevel=info

# With specific queues
celery -A app.tasks.celery_app worker -Q downloads,analysis --loglevel=info

# With concurrency
celery -A app.tasks.celery_app worker --concurrency=4 --loglevel=info
```

### Production

```bash
# With autoscaling
celery -A app.tasks.celery_app worker \
  --autoscale=10,3 \
  --loglevel=info \
  --logfile=/app/logs/celery.log

# Multiple workers for different queues
celery -A app.tasks.celery_app worker -Q downloads --concurrency=2 --loglevel=info &
celery -A app.tasks.celery_app worker -Q analysis --concurrency=4 --loglevel=info &
```

## Monitoring Tasks

### Using Task Utils

```python
from app.tasks.task_utils import get_task_status, get_active_tasks

# Get task status
status = get_task_status("task-id-here")
print(status)

# Get all active tasks
active = get_active_tasks()
print(active)
```

### Using Flower (Optional)

```bash
# Install Flower
pip install flower

# Run Flower
celery -A app.tasks.celery_app flower --port=5555
```

Access at: http://localhost:5555

## Task States

- **PENDING**: Task is waiting to be executed
- **PROGRESS**: Task is running (custom state)
- **SUCCESS**: Task completed successfully
- **FAILURE**: Task failed with error
- **RETRY**: Task is being retried
- **REVOKED**: Task was cancelled

## Configuration

Key settings in `celery_app.py`:

- **task_time_limit**: 3600 seconds (1 hour max)
- **task_soft_time_limit**: 3000 seconds (50 minutes soft limit)
- **worker_prefetch_multiplier**: 1 (one task at a time)
- **worker_max_tasks_per_child**: 50 (restart worker after 50 tasks)

## Error Handling

Tasks automatically retry on failure:

- **Download tasks**: 3 retries with exponential backoff
- **Analysis tasks**: 2 retries with exponential backoff

## Database Sessions

Each task creates its own database session:

```python
db = SessionLocal()
try:
    # Do work
    db.commit()
finally:
    db.close()
```

## Best Practices

1. **Keep tasks idempotent**: Tasks should produce the same result if run multiple times
2. **Update progress**: Use `self.update_state()` to track progress
3. **Handle errors**: Always use try/except and update analysis status on failure
4. **Close resources**: Always close database sessions in finally blocks
5. **Log everything**: Use logger for debugging and monitoring
