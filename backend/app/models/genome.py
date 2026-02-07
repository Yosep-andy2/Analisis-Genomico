"""Genome model for storing downloaded genome information."""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Genome(Base):
    """
    Genome model representing a downloaded genome from NCBI.
    
    Attributes:
        id: Primary key
        accession: NCBI accession number (e.g., NC_000913.3)
        organism_name: Scientific name of the organism
        genome_size: Size of genome in base pairs
        gc_content: GC content percentage
        download_date: Timestamp when genome was downloaded
        file_path: Path to the downloaded GenBank file
        metadata: Additional metadata as JSON
    """
    
    __tablename__ = "genomes"
    
    id = Column(Integer, primary_key=True, index=True)
    accession = Column(String(50), unique=True, nullable=False, index=True)
    organism_name = Column(String(255), nullable=False)
    genome_size = Column(Integer)
    gc_content = Column(Numeric(5, 2))
    download_date = Column(DateTime(timezone=True), server_default=func.now())
    file_path = Column(String(500))
    metadata = Column(JSON)
    
    # Relationships
    analyses = relationship("Analysis", back_populates="genome", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Genome(accession='{self.accession}', organism='{self.organism_name}')>"
