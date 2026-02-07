"""Validation model for storing result validation data."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Validation(Base):
    """
    Validation model representing result validation against references.
    
    Attributes:
        id: Primary key
        analysis_id: Foreign key to analysis
        reference_accession: Accession number of reference genome
        deviations: Deviation data as JSON
        validation_status: Status (passed, warning, failed)
        created_at: Timestamp when validation was created
    """
    
    __tablename__ = "validations"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False, index=True)
    reference_accession = Column(String(50))
    deviations = Column(JSON)
    validation_status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    analysis = relationship("Analysis", back_populates="validations")
    
    def __repr__(self):
        return f"<Validation(id={self.id}, status='{self.validation_status}')>"
