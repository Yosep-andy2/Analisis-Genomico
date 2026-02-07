"""Codon analyzer for identifying start and stop codons in genomes."""

import re
from typing import Dict, List, Any
from Bio import SeqIO
from app.analyzers.base_analyzer import BaseAnalyzer
from app.core.logging import logger


class CodonAnalyzer(BaseAnalyzer):
    """
    Analyzer for counting and analyzing codons in genome sequences.
    
    Analyzes:
    - Start codons (ATG)
    - Stop codons (TAA, TAG, TGA)
    - Codon frequencies and distributions
    """
    
    def __init__(self):
        """Initialize the codon analyzer."""
        super().__init__()
        self.start_codon = "ATG"
        self.stop_codons = ["TAA", "TAG", "TGA"]
    
    def analyze(self, genbank_file: str) -> Dict[str, Any]:
        """
        Analyze codons in a GenBank file.
        
        Args:
            genbank_file: Path to GenBank file
            
        Returns:
            Dictionary with codon analysis results
        """
        if not self.validate_file(genbank_file):
            raise FileNotFoundError(f"GenBank file not found: {genbank_file}")
        
        logger.info(f"Starting codon analysis for {genbank_file}")
        
        # Read GenBank file
        record = SeqIO.read(genbank_file, "genbank")
        sequence = str(record.seq).upper()
        
        # Analyze start codons
        start_codon_results = self.count_start_codons(sequence)
        
        # Analyze stop codons
        stop_codon_results = self.count_stop_codons(sequence)
        
        results = {
            "start_codons": start_codon_results,
            "stop_codons": stop_codon_results,
            "genome_length": len(sequence)
        }
        
        logger.info("Codon analysis completed")
        return results
    
    def count_start_codons(self, sequence: str) -> Dict[str, Any]:
        """
        Count all ATG start codons in the sequence.
        
        Args:
            sequence: DNA sequence string
            
        Returns:
            Dictionary with start codon counts and statistics
        """
        # Find all ATG positions
        atg_pattern = re.compile(self.start_codon)
        positions = [m.start() for m in atg_pattern.finditer(sequence)]
        
        total_count = len(positions)
        density_per_kb = (total_count / len(sequence)) * 1000 if len(sequence) > 0 else 0
        
        return {
            "codon": self.start_codon,
            "total_count": total_count,
            "positions": positions[:100],  # Store first 100 positions to avoid huge data
            "density_per_kb": round(density_per_kb, 2),
            "note": "ATG is the start codon for translation"
        }
    
    def count_stop_codons(self, sequence: str) -> Dict[str, Any]:
        """
        Count all stop codons (TAA, TAG, TGA) in the sequence.
        
        Args:
            sequence: DNA sequence string
            
        Returns:
            Dictionary with stop codon counts and frequencies
        """
        codon_counts = {}
        total_stops = 0
        
        # Count each stop codon
        for codon in self.stop_codons:
            pattern = re.compile(codon)
            matches = pattern.findall(sequence)
            count = len(matches)
            codon_counts[codon] = count
            total_stops += count
        
        # Calculate frequencies
        codon_frequencies = {}
        for codon, count in codon_counts.items():
            frequency = (count / total_stops * 100) if total_stops > 0 else 0
            codon_frequencies[codon] = {
                "count": count,
                "frequency_percent": round(frequency, 2)
            }
        
        return {
            "codons": codon_frequencies,
            "total_stop_codons": total_stops,
            "density_per_kb": round((total_stops / len(sequence)) * 1000, 2) if len(sequence) > 0 else 0,
            "note": "TAA, TAG, and TGA are stop codons for translation"
        }
    
    def compare_with_genes(self, start_codon_count: int, gene_count: int) -> Dict[str, Any]:
        """
        Compare start codon count with annotated gene count.
        
        Args:
            start_codon_count: Number of ATG codons found
            gene_count: Number of annotated genes
            
        Returns:
            Comparison statistics
        """
        ratio = start_codon_count / gene_count if gene_count > 0 else 0
        
        return {
            "start_codons": start_codon_count,
            "annotated_genes": gene_count,
            "ratio": round(ratio, 2),
            "interpretation": self._interpret_ratio(ratio)
        }
    
    def _interpret_ratio(self, ratio: float) -> str:
        """
        Interpret the ATG to gene ratio.
        
        Args:
            ratio: Ratio of ATG codons to genes
            
        Returns:
            Interpretation string
        """
        if ratio < 1:
            return "Fewer ATG codons than genes (unexpected)"
        elif ratio < 2:
            return "Close to 1:1 ratio (most ATGs are gene starts)"
        elif ratio < 5:
            return "Moderate ratio (some ATGs are not gene starts)"
        else:
            return "High ratio (many ATGs are not gene starts)"
