"""Pydantic schemas for analysis-related requests and responses."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AnalysisRequest(BaseModel):
    """Schema for analysis request."""
    
    accession: str = Field(..., description="NCBI accession number to analyze")
    
    class Config:
        json_schema_extra = {
            "example": {
                "accession": "NC_000913.3"
            }
        }


class AnalysisStatus(BaseModel):
    """Schema for analysis status response."""
    
    analysis_id: int = Field(..., description="Analysis ID")
    task_id: str = Field(..., description="Celery task ID")
    status: str = Field(..., description="Status: pending, running, completed, failed")
    progress: Optional[float] = Field(0.0, description="Progress percentage (0-100)")
    message: Optional[str] = Field(None, description="Status message")
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "analysis_id": 1,
                "task_id": "abc-123-def-456",
                "status": "running",
                "progress": 45.0,
                "message": "Analyzing genes...",
                "started_at": "2024-01-15T10:30:00Z",
                "completed_at": None
            }
        }


class AnalysisResponse(BaseModel):
    """Schema for analysis response."""
    
    id: int
    genome_id: int
    task_id: Optional[str] = None
    status: str
    progress: float
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True
