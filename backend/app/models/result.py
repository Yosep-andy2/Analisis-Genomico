"""Result model for storing analysis results."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Result(Base):
    """
    Result model representing analysis results.
    
    Attributes:
        id: Primary key
        analysis_id: Foreign key to analysis
        result_type: Type of result (codon_analysis, gene_stats, genome_stats)
        data: Result data as JSON
        created_at: Timestamp when result was created
    """
    
    __tablename__ = "results"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False, index=True)
    result_type = Column(String(50), nullable=False)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    analysis = relationship("Analysis", back_populates="results")
    
    def __repr__(self):
        return f"<Result(id={self.id}, type='{self.result_type}')>"
