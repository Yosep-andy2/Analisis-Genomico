"""Gene analyzer for extracting and analyzing genes from GenBank files."""

from typing import Dict, List, Any
import statistics
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
from app.analyzers.base_analyzer import BaseAnalyzer
from app.core.logging import logger


class GeneAnalyzer(BaseAnalyzer):
    """
    Analyzer for extracting and analyzing genes from genome annotations.
    
    Analyzes:
    - Gene count and distribution
    - Gene lengths
    - GC content per gene
    - Gene statistics (mean, median, etc.)
    """
    
    def analyze(self, genbank_file: str) -> Dict[str, Any]:
        """
        Analyze genes in a GenBank file.
        
        Args:
            genbank_file: Path to GenBank file
            
        Returns:
            Dictionary with gene analysis results
        """
        if not self.validate_file(genbank_file):
            raise FileNotFoundError(f"GenBank file not found: {genbank_file}")
        
        logger.info(f"Starting gene analysis for {genbank_file}")
        
        # Extract genes
        genes = self.extract_genes(genbank_file)
        
        # Calculate statistics
        stats = self.calculate_gene_statistics(genes)
        
        results = {
            "genes": genes[:50],  # Store first 50 genes to avoid huge data
            "total_genes": len(genes),
            "statistics": stats
        }
        
        logger.info(f"Gene analysis completed. Found {len(genes)} genes")
        return results
    
    def extract_genes(self, genbank_file: str) -> List[Dict[str, Any]]:
        """
        Extract all genes from GenBank file.
        
        Args:
            genbank_file: Path to GenBank file
            
        Returns:
            List of gene dictionaries
        """
        record = SeqIO.read(genbank_file, "genbank")
        genes = []
        
        for feature in record.features:
            if feature.type == "CDS":  # Coding DNA Sequence
                try:
                    # Extract sequence
                    sequence = feature.extract(record.seq)
                    
                    # Get gene information
                    gene_info = {
                        "gene_name": feature.qualifiers.get("gene", ["Unknown"])[0],
                        "locus_tag": feature.qualifiers.get("locus_tag", [""])[0],
                        "product": feature.qualifiers.get("product", ["Unknown protein"])[0],
                        "location": str(feature.location),
                        "start": int(feature.location.start),
                        "end": int(feature.location.end),
                        "length": len(sequence),
                        "gc_content": round(gc_fraction(sequence) * 100, 2),
                        "strand": "+" if feature.location.strand == 1 else "-"
                    }
                    
                    genes.append(gene_info)
                    
                except Exception as e:
                    logger.warning(f"Error extracting gene: {e}")
                    continue
        
        return genes
    
    def calculate_gene_statistics(self, genes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate statistics for extracted genes.
        
        Args:
            genes: List of gene dictionaries
            
        Returns:
            Dictionary with gene statistics
        """
        if not genes:
            return {
                "total_genes": 0,
                "error": "No genes found"
            }
        
        # Extract metrics
        lengths = [g["length"] for g in genes]
        gc_contents = [g["gc_content"] for g in genes]
        
        # Count strands
        forward_strand = sum(1 for g in genes if g["strand"] == "+")
        reverse_strand = sum(1 for g in genes if g["strand"] == "-")
        
        # Calculate statistics
        stats = {
            "total_genes": len(genes),
            "length_stats": {
                "mean": round(statistics.mean(lengths), 2),
                "median": statistics.median(lengths),
                "min": min(lengths),
                "max": max(lengths),
                "stdev": round(statistics.stdev(lengths), 2) if len(lengths) > 1 else 0
            },
            "gc_content_stats": {
                "mean": round(statistics.mean(gc_contents), 2),
                "median": round(statistics.median(gc_contents), 2),
                "min": round(min(gc_contents), 2),
                "max": round(max(gc_contents), 2)
            },
            "strand_distribution": {
                "forward": forward_strand,
                "reverse": reverse_strand,
                "forward_percent": round((forward_strand / len(genes)) * 100, 2),
                "reverse_percent": round((reverse_strand / len(genes)) * 100, 2)
            }
        }
        
        return stats
    
    def get_length_distribution(self, genes: List[Dict[str, Any]], bin_size: int = 100) -> Dict[str, List]:
        """
        Get distribution of gene lengths in bins.
        
        Args:
            genes: List of gene dictionaries
            bin_size: Size of each bin in base pairs
            
        Returns:
            Dictionary with bins and counts
        """
        lengths = [g["length"] for g in genes]
        max_length = max(lengths) if lengths else 0
        
        # Create bins
        bins = list(range(0, max_length + bin_size, bin_size))
        counts = [0] * len(bins)
        
        # Count genes in each bin
        for length in lengths:
            bin_index = min(length // bin_size, len(bins) - 1)
            counts[bin_index] += 1
        
        return {
            "bins": bins,
            "counts": counts,
            "bin_size": bin_size
        }
