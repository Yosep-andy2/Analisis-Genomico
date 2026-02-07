"""Genome analyzer for calculating genome-wide statistics."""

from typing import Dict, Any
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
from app.analyzers.base_analyzer import BaseAnalyzer
from app.core.logging import logger


class GenomeAnalyzer(BaseAnalyzer):
    """
    Analyzer for genome-wide statistics.
    
    Analyzes:
    - Genome size
    - GC content
    - Nucleotide composition
    - Coding density
    """
    
    def analyze(self, genbank_file: str) -> Dict[str, Any]:
        """
        Analyze genome-wide statistics.
        
        Args:
            genbank_file: Path to GenBank file
            
        Returns:
            Dictionary with genome statistics
        """
        if not self.validate_file(genbank_file):
            raise FileNotFoundError(f"GenBank file not found: {genbank_file}")
        
        logger.info(f"Starting genome analysis for {genbank_file}")
        
        # Read GenBank file
        record = SeqIO.read(genbank_file, "genbank")
        
        # Calculate statistics
        stats = self.calculate_genome_stats(record)
        
        logger.info("Genome analysis completed")
        return stats
    
    def calculate_genome_stats(self, record) -> Dict[str, Any]:
        """
        Calculate comprehensive genome statistics.
        
        Args:
            record: BioPython SeqRecord object
            
        Returns:
            Dictionary with genome statistics
        """
        sequence = str(record.seq).upper()
        
        # Basic stats
        genome_size = len(sequence)
        gc_content = gc_fraction(record.seq) * 100
        
        # Nucleotide composition
        composition = self._calculate_composition(sequence)
        
        # Count genes
        gene_count = sum(1 for f in record.features if f.type == "CDS")
        
        # Calculate coding length
        coding_length = sum(
            len(f.extract(record.seq)) 
            for f in record.features 
            if f.type == "CDS"
        )
        
        # Coding density
        coding_density = (coding_length / genome_size * 100) if genome_size > 0 else 0
        
        stats = {
            "organism": record.description,
            "accession": record.id,
            "genome_size": genome_size,
            "gc_content": round(gc_content, 2),
            "nucleotide_composition": composition,
            "gene_count": gene_count,
            "coding_length": coding_length,
            "coding_density": round(coding_density, 2),
            "average_gene_length": round(coding_length / gene_count, 2) if gene_count > 0 else 0
        }
        
        return stats
    
    def _calculate_composition(self, sequence: str) -> Dict[str, Any]:
        """
        Calculate nucleotide composition.
        
        Args:
            sequence: DNA sequence string
            
        Returns:
            Dictionary with nucleotide counts and percentages
        """
        total = len(sequence)
        
        composition = {}
        for nucleotide in ["A", "T", "G", "C"]:
            count = sequence.count(nucleotide)
            percentage = (count / total * 100) if total > 0 else 0
            composition[nucleotide] = {
                "count": count,
                "percentage": round(percentage, 2)
            }
        
        # Calculate AT and GC content
        at_content = composition["A"]["percentage"] + composition["T"]["percentage"]
        gc_content = composition["G"]["percentage"] + composition["C"]["percentage"]
        
        composition["AT_content"] = round(at_content, 2)
        composition["GC_content"] = round(gc_content, 2)
        
        return composition
    
    def calculate_gc_sliding_window(self, sequence: str, window_size: int = 1000, step: int = 500) -> Dict[str, List]:
        """
        Calculate GC content in sliding windows across the genome.
        
        Args:
            sequence: DNA sequence string
            window_size: Size of sliding window
            step: Step size for window movement
            
        Returns:
            Dictionary with positions and GC values
        """
        positions = []
        gc_values = []
        
        for i in range(0, len(sequence) - window_size, step):
            window = sequence[i:i + window_size]
            gc = (window.count("G") + window.count("C")) / len(window) * 100
            positions.append(i + window_size // 2)  # Center of window
            gc_values.append(round(gc, 2))
        
        return {
            "positions": positions,
            "gc_values": gc_values,
            "window_size": window_size,
            "step": step
        }
