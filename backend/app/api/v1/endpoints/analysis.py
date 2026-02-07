"""Analysis endpoints for managing genome analysis tasks."""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.analysis import AnalysisRequest, AnalysisStatus, AnalysisResponse
from app.services.ncbi_service import NCBIService
from app.models.genome import Genome
from app.models.analysis import Analysis
from app.core.logging import logger
from app.core.exceptions import NCBIException
import uuid

router = APIRouter()


@router.post("/start", response_model=AnalysisStatus, status_code=202)
async def start_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Start a new genome analysis.
    
    - **accession**: NCBI accession number to analyze
    
    This endpoint will:
    1. Download the genome from NCBI (if not already downloaded)
    2. Create a genome record in the database
    3. Start an asynchronous analysis task
    4. Return the analysis status
    
    The analysis runs in the background. Use the returned analysis_id
    to check the status with GET /analysis/{analysis_id}
    """
    logger.info(f"Starting analysis for: {request.accession}")
    
    try:
        # Check if genome already exists
        genome = db.query(Genome).filter(Genome.accession == request.accession).first()
        
        if not genome:
            # Download genome
            ncbi_service = NCBIService()
            file_path = ncbi_service.download_genome(request.accession)
            metadata = ncbi_service.get_genome_metadata(request.accession)
            
            # Create genome record
            genome = Genome(
                accession=request.accession,
                organism_name=metadata.get("organism", "Unknown"),
                genome_size=metadata.get("length", 0),
                file_path=file_path,
                metadata=metadata
            )
            db.add(genome)
            db.commit()
            db.refresh(genome)
            
            logger.info(f"Genome downloaded and saved: {genome.id}")
        else:
            logger.info(f"Genome already exists: {genome.id}")
        
        # Create analysis record
        task_id = str(uuid.uuid4())
        analysis = Analysis(
            genome_id=genome.id,
            task_id=task_id,
            status="pending",
            progress=0.0,
            message="Analysis queued"
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        # TODO: Start Celery task here
        # For now, we'll just mark it as pending
        logger.info(f"Analysis created: {analysis.id}")
        
        return AnalysisStatus(
            analysis_id=analysis.id,
            task_id=task_id,
            status="pending",
            progress=0.0,
            message="Analysis queued for processing",
            started_at=analysis.started_at
        )
        
    except NCBIException as e:
        logger.error(f"NCBI error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error starting analysis: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{analysis_id}", response_model=AnalysisStatus)
async def get_analysis_status(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the status of an analysis.
    
    - **analysis_id**: Analysis ID returned from POST /analysis/start
    
    Returns the current status, progress, and any error messages.
    """
    logger.info(f"Fetching analysis status: {analysis_id}")
    
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return AnalysisStatus(
        analysis_id=analysis.id,
        task_id=analysis.task_id,
        status=analysis.status,
        progress=analysis.progress,
        message=analysis.message,
        started_at=analysis.started_at,
        completed_at=analysis.completed_at
    )


@router.get("/", response_model=list[AnalysisResponse])
async def list_analyses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all analyses.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    
    Returns a list of all analyses ordered by most recent first.
    """
    logger.info(f"Listing analyses: skip={skip}, limit={limit}")
    
    analyses = db.query(Analysis)\
        .order_by(Analysis.started_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return analyses
