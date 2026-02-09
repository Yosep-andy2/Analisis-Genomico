from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "version": settings.VERSION
    }

@patch('app.services.ncbi_service.NCBIService.search_genomes')
def test_search_genomes(mock_search):
    """Test genome search endpoint."""
    # Mock return value
    mock_search.return_value = [
        {
            "accession": "NC_000913.3",
            "title": "Escherichia coli str. K-12 substr. MG1655",
            "organism": "Escherichia coli",
            "length": 4641652,
            "update_date": "2024/01/01"
        }
    ]
    
    response = client.get("/api/v1/genomes/search?query=ecoli")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['accession'] == "NC_000913.3"

@patch('app.db.session.get_db')
@patch('app.tasks.analysis_tasks.analyze_genome_task.apply_async')
def test_start_analysis(mock_celery, mock_get_db):
    """Test starting an analysis."""
    # Mock DB session
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    
    # Mock genome query to return None (trigger download)
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Mock NCBIService download and metadata
    with patch('app.api.v1.endpoints.analysis.NCBIService') as MockNCBIService:
        service_instance = MockNCBIService.return_value
        service_instance.download_genome.return_value = "/tmp/genome.gb"
        service_instance.get_genome_metadata.return_value = {
            "organism": "E. coli",
            "length": 4600000
        }
        
        # Mock Celery task
        mock_task = MagicMock()
        mock_task.id = "task-123"
        mock_celery.return_value = mock_task
        
        response = client.post(
            "/api/v1/analysis/start",
            json={"accession": "NC_000913.3"}
        )
        
        # We expect 202 Accepted
        assert response.status_code == 202
        data = response.json()
        assert data['status'] == "pending"
        assert 'task_id' in data
