"""Results endpoints for retrieving analysis results."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.analysis import Analysis
from app.models.result import Result
from app.models.validation import Validation
from app.schemas.result import ResultResponse, CompleteAnalysisResult
from app.core.logging import logger

router = APIRouter()


@router.get("/{analysis_id}", response_model=CompleteAnalysisResult)
async def get_analysis_results(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Get complete results for an analysis.
    
    - **analysis_id**: Analysis ID
    
    Returns all analysis results including:
    - Codon analysis (start and stop codons)
    - Gene statistics
    - Genome statistics
    - Validation results
    - Chart URLs (if available)
    
    Only available for completed analyses.
    """
    logger.info(f"Fetching results for analysis: {analysis_id}")
    
    # Get analysis
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if analysis.status != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Analysis not completed. Current status: {analysis.status}"
        )
    
    # Get genome info
    genome = analysis.genome
    
    # Get results
    results = db.query(Result).filter(Result.analysis_id == analysis_id).all()
    
    # Organize results by type
    result_data = {}
    for result in results:
        result_data[result.result_type] = result.data
    
    # Get validation
    validation = db.query(Validation).filter(Validation.analysis_id == analysis_id).first()
    validation_data = None
    if validation:
        validation_data = {
            "status": validation.validation_status,
            "reference_accession": validation.reference_accession,
            "validations": validation.deviations,
            "validated": True
        }
    
    return CompleteAnalysisResult(
        analysis_id=analysis.id,
        genome_accession=genome.accession,
        organism=genome.organism_name,
        status=analysis.status,
        codon_analysis=result_data.get("codon_analysis"),
        gene_stats=result_data.get("gene_stats"),
        genome_stats=result_data.get("genome_stats"),
        validation=validation_data,
        charts=result_data.get("charts")
    )


@router.get("/{analysis_id}/raw", response_model=List[ResultResponse])
async def get_raw_results(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Get raw result records for an analysis.
    
    - **analysis_id**: Analysis ID
    
    Returns all result records as stored in the database.
    """
    logger.info(f"Fetching raw results for analysis: {analysis_id}")
    
    # Check analysis exists
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    # Get results
    results = db.query(Result).filter(Result.analysis_id == analysis_id).all()
    
    return results
