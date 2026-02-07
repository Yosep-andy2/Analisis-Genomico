"""Genome endpoints for searching and retrieving genome information."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.services.ncbi_service import NCBIService
from app.schemas.genome import GenomeSearchResult, GenomeDetail
from app.core.logging import logger
from app.core.exceptions import NCBIException, GenomeNotFoundException

router = APIRouter()


@router.get("/search", response_model=List[GenomeSearchResult])
async def search_genomes(
    query: str = Query(..., min_length=3, description="Search query (organism name or accession)"),
    limit: int = Query(20, le=100, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Search for genomes in NCBI GenBank.
    
    - **query**: Organism name or accession number (minimum 3 characters)
    - **limit**: Maximum number of results (default: 20, max: 100)
    
    Returns a list of matching genomes with basic information.
    """
    logger.info(f"Searching genomes: query='{query}', limit={limit}")
    
    try:
        ncbi_service = NCBIService()
        results = ncbi_service.search_genomes(query, max_results=limit)
        
        logger.info(f"Found {len(results)} genomes")
        return results
        
    except NCBIException as e:
        logger.error(f"NCBI search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in genome search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{accession}", response_model=GenomeDetail)
async def get_genome_details(
    accession: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed information for a specific genome.
    
    - **accession**: NCBI accession number (e.g., NC_000913.3)
    
    Returns detailed metadata for the genome.
    """
    logger.info(f"Fetching genome details: {accession}")
    
    try:
        ncbi_service = NCBIService()
        metadata = ncbi_service.get_genome_metadata(accession)
        
        return metadata
        
    except GenomeNotFoundException as e:
        logger.warning(f"Genome not found: {accession}")
        raise HTTPException(status_code=404, detail=str(e))
    except NCBIException as e:
        logger.error(f"NCBI error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error fetching genome: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
