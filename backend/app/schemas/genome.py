"""Pydantic schemas for genome-related requests and responses."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GenomeSearchResult(BaseModel):
    """Schema for genome search result."""
    
    accession: str = Field(..., description="NCBI accession number")
    title: str = Field(..., description="Genome title")
    organism: str = Field(..., description="Organism name")
    length: int = Field(..., description="Genome length in base pairs")
    update_date: str = Field(..., description="Last update date")
    gi: Optional[str] = Field(None, description="GenInfo Identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "accession": "NC_000913.3",
                "title": "Escherichia coli str. K-12 substr. MG1655, complete genome",
                "organism": "Escherichia coli str. K-12 substr. MG1655",
                "length": 4641652,
                "update_date": "2023-01-15",
                "gi": "556503834"
            }
        }


class GenomeDetail(BaseModel):
    """Schema for detailed genome information."""
    
    accession: str
    title: str
    organism: str
    length: int
    create_date: str
    update_date: str
    taxonomy: str
    gi: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "accession": "NC_000913.3",
                "title": "Escherichia coli str. K-12 substr. MG1655, complete genome",
                "organism": "Escherichia coli str. K-12 substr. MG1655",
                "length": 4641652,
                "create_date": "2013-09-26",
                "update_date": "2023-01-15",
                "taxonomy": "511145",
                "gi": "556503834"
            }
        }


class GenomeBase(BaseModel):
    """Base schema for genome."""
    
    accession: str
    organism_name: str
    genome_size: Optional[int] = None
    gc_content: Optional[float] = None


class GenomeCreate(GenomeBase):
    """Schema for creating a genome record."""
    
    file_path: Optional[str] = None
    metadata: Optional[dict] = None


class GenomeResponse(GenomeBase):
    """Schema for genome response."""
    
    id: int
    download_date: datetime
    file_path: Optional[str] = None
    
    class Config:
        from_attributes = True
