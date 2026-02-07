"""Download tasks for fetching genomes from NCBI."""

from celery import Task
from app.tasks.celery_app import celery_app
from app.services.ncbi_service import NCBIService
from app.core.logging import logger
from app.core.exceptions import NCBIException


class DownloadTask(Task):
    """Base task for downloads with error handling."""
    
    autoretry_for = (NCBIException,)
    retry_kwargs = {"max_retries": 3}
    retry_backoff = True


@celery_app.task(base=DownloadTask, bind=True, name="download_genome")
def download_genome_task(self, accession: str) -> dict:
    """
    Download a genome from NCBI.
    
    Args:
        accession: NCBI accession number
        
    Returns:
        Dictionary with download results
    """
    logger.info(f"Task {self.request.id}: Downloading genome {accession}")
    
    try:
        # Update task state
        self.update_state(
            state="PROGRESS",
            meta={
                "current": 0,
                "total": 100,
                "status": "Connecting to NCBI..."
            }
        )
        
        # Download genome
        ncbi_service = NCBIService()
        
        self.update_state(
            state="PROGRESS",
            meta={
                "current": 30,
                "total": 100,
                "status": "Downloading genome..."
            }
        )
        
        file_path = ncbi_service.download_genome(accession)
        
        self.update_state(
            state="PROGRESS",
            meta={
                "current": 80,
                "total": 100,
                "status": "Validating file..."
            }
        )
        
        # Get metadata
        metadata = ncbi_service.get_genome_metadata(accession)
        
        logger.info(f"Task {self.request.id}: Download completed")
        
        return {
            "status": "completed",
            "accession": accession,
            "file_path": file_path,
            "metadata": metadata
        }
        
    except Exception as e:
        logger.error(f"Task {self.request.id}: Download failed - {e}")
        raise
