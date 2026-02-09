# API Documentation

The Genomic Analysis Platform provides a RESTful API documented using OpenAPI (Swagger).

## Interactive Documentation

Once the backend is running, you can access:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs) - Interactive exploration and testing.
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc) - Alternative documentation view.

## Core Endpoints

### 1. Genomes

- **Search Genomes**
  - `GET /api/v1/genomes/search?query={term}`
  - Searches NCBI GenBank for genomes matching the query.

- **Get Genome Details**
  - `GET /api/v1/genomes/{accession}`
  - Retrieves detailed metadata for a specific genome.

### 2. Analysis

- **Start Analysis**
  - `POST /api/v1/analysis/start`
  - Body: `{"accession": "NC_000913.3"}`
  - Initiates the background analysis task.

- **Check Status**
  - `GET /api/v1/analysis/{task_id}/status`
  - Returns the current progress (0-100%) and status (pending, running, completed, failed).

- **List Analyses**
  - `GET /api/v1/analysis/`
  - Lists historical analysis requests.

### 3. Results

- **Get Complete Results**
  - `GET /api/v1/results/{analysis_id}/complete`
  - Returns full analysis data including:
    - Codon analysis
    - Gene statistics
    - Genome statistics
    - Validation results
    - Metadata

## Data Models

Refer to the Swagger UI Schema section for detailed JSON structures of request and response objects.
