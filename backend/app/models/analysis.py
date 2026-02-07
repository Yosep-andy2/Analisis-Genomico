"""Analysis model for tracking genome analysis tasks."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Analysis(Base):
    """
    Analysis model representing a genome analysis task.
    
    Attributes:
        id: Primary key
        genome_id: Foreign key to genome
        task_id: Celery task ID
        status: Analysis status (pending, running, completed, failed)
        progress: Progress percentage (0-100)
        started_at: Timestamp when analysis started
        completed_at: Timestamp when analysis completed
        error_message: Error message if analysis failed
        message: Current status message
    """
    
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    genome_id = Column(Integer, ForeignKey("genomes.id"), nullable=False)
    task_id = Column(String(100), unique=True, index=True)
    status = Column(String(50), default="pending", index=True)
    progress = Column(Float, default=0.0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    message = Column(String(500))
    
    # Relationships
    genome = relationship("Genome", back_populates="analyses")
    results = relationship("Result", back_populates="analysis", cascade="all, delete-orphan")
    validations = relationship("Validation", back_populates="analysis", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Analysis(id={self.id}, status='{self.status}', progress={self.progress})>"
