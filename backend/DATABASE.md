# Database Migrations Guide

## Database Schema

### Tables

#### genomes
Stores downloaded genome information from NCBI.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| accession | String(50) | NCBI accession (unique, indexed) |
| organism_name | String(255) | Scientific name |
| genome_size | Integer | Size in base pairs |
| gc_content | Numeric(5,2) | GC content percentage |
| download_date | DateTime | Download timestamp |
| file_path | String(500) | Path to GenBank file |
| metadata | JSON | Additional metadata |

#### analyses
Tracks genome analysis tasks.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| genome_id | Integer | Foreign key to genomes |
| task_id | String(100) | Celery task ID (unique, indexed) |
| status | String(50) | Status (pending/running/completed/failed) |
| progress | Float | Progress 0-100 |
| started_at | DateTime | Start timestamp |
| completed_at | DateTime | Completion timestamp |
| error_message | Text | Error message if failed |
| message | String(500) | Current status message |

#### results
Stores analysis results.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| analysis_id | Integer | Foreign key to analyses |
| result_type | String(50) | Type (codon_analysis/gene_stats/genome_stats) |
| data | JSON | Result data |
| created_at | DateTime | Creation timestamp |

#### validations
Stores validation results.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| analysis_id | Integer | Foreign key to analyses |
| reference_accession | String(50) | Reference genome accession |
| deviations | JSON | Deviation data |
| validation_status | String(20) | Status (passed/warning/failed) |
| created_at | DateTime | Creation timestamp |

## Relationships

```
Genome (1) ──< (N) Analysis
Analysis (1) ──< (N) Result
Analysis (1) ──< (N) Validation
```

## Using Alembic

### Create Initial Migration

```bash
cd backend
alembic revision --autogenerate -m "Initial schema"
```

### Apply Migrations

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade one version
alembic upgrade +1

# Downgrade one version
alembic downgrade -1

# Show current version
alembic current

# Show migration history
alembic history
```

### Quick Database Setup

```bash
# Using the init script (creates tables directly)
python scripts/init_db.py
```

## Example Queries

### Create a genome record

```python
from app.models.genome import Genome
from app.db.session import SessionLocal

db = SessionLocal()
genome = Genome(
    accession="NC_000913.3",
    organism_name="Escherichia coli K-12 MG1655",
    genome_size=4641652,
    gc_content=50.8,
    file_path="/app/data/genomes/NC_000913.3.gb"
)
db.add(genome)
db.commit()
```

### Query genomes

```python
# Get by accession
genome = db.query(Genome).filter(Genome.accession == "NC_000913.3").first()

# Get all genomes
genomes = db.query(Genome).all()

# Get with analyses
genome = db.query(Genome).filter(Genome.id == 1).first()
analyses = genome.analyses
```

### Create analysis with results

```python
from app.models.analysis import Analysis
from app.models.result import Result

analysis = Analysis(
    genome_id=1,
    task_id="abc-123",
    status="completed",
    progress=100.0
)
db.add(analysis)
db.commit()

result = Result(
    analysis_id=analysis.id,
    result_type="codon_analysis",
    data={
        "start_codons": {"total": 4500, "density": 0.97},
        "stop_codons": {"TAA": 2700, "TAG": 400, "TGA": 1300}
    }
)
db.add(result)
db.commit()
```
