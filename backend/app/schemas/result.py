"""Pydantic schemas for result-related responses."""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime


class ResultResponse(BaseModel):
    """Schema for result response."""
    
    id: int
    analysis_id: int
    result_type: str = Field(..., description="Type: codon_analysis, gene_stats, genome_stats")
    data: Dict[str, Any] = Field(..., description="Result data")
    created_at: datetime
    
    class Config:
        from_attributes = True


class CodonAnalysisResult(BaseModel):
    """Schema for codon analysis result."""
    
    start_codons: Dict[str, Any]
    stop_codons: Dict[str, Any]
    genome_length: int


class GeneStatsResult(BaseModel):
    """Schema for gene statistics result."""
    
    total_genes: int
    statistics: Dict[str, Any]
    genes: Optional[List[Dict[str, Any]]] = None


class GenomeStatsResult(BaseModel):
    """Schema for genome statistics result."""
    
    organism: str
    accession: str
    genome_size: int
    gc_content: float
    nucleotide_composition: Dict[str, Any]
    gene_count: int
    coding_density: float


class ValidationResult(BaseModel):
    """Schema for validation result."""
    
    status: str = Field(..., description="Status: passed, warning, failed, no_reference")
    reference_accession: Optional[str] = None
    reference_organism: Optional[str] = None
    validations: Optional[Dict[str, Any]] = None
    validated: bool
    reference_citation: Optional[str] = None


class CompleteAnalysisResult(BaseModel):
    """Schema for complete analysis results."""
    
    analysis_id: int
    genome_accession: str
    organism: str
    status: str
    codon_analysis: Optional[CodonAnalysisResult] = None
    gene_stats: Optional[GeneStatsResult] = None
    genome_stats: Optional[GenomeStatsResult] = None
    validation: Optional[ValidationResult] = None
    charts: Optional[Dict[str, str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_id": 1,
                "genome_accession": "NC_000913.3",
                "organism": "Escherichia coli K-12 MG1655",
                "status": "completed",
                "codon_analysis": {
                    "start_codons": {"total_count": 4500, "density_per_kb": 0.97},
                    "stop_codons": {"total_stop_codons": 4400},
                    "genome_length": 4641652
                },
                "gene_stats": {
                    "total_genes": 4321,
                    "statistics": {"length_stats": {"mean": 948}}
                },
                "genome_stats": {
                    "genome_size": 4641652,
                    "gc_content": 50.8,
                    "coding_density": 87.8
                }
            }
        }
