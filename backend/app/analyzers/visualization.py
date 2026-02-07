"""Visualization generator for creating analysis charts."""

from typing import Dict, List, Any
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
from pathlib import Path
from app.core.logging import logger


class VisualizationGenerator:
    """
    Generator for creating visualization charts from analysis data.
    
    Creates:
    - Codon frequency bar charts
    - Gene length histograms
    - GC content plots
    - Nucleotide composition pie charts
    """
    
    def __init__(self, output_dir: str = "./data/results"):
        """
        Initialize visualization generator.
        
        Args:
            output_dir: Directory to save chart images
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def create_stop_codon_chart(self, stop_codon_data: Dict[str, Any], output_file: str = None) -> str:
        """
        Create bar chart for stop codon frequencies.
        
        Args:
            stop_codon_data: Stop codon analysis data
            output_file: Optional output file path
            
        Returns:
            Path to saved chart
        """
        codons = stop_codon_data.get("codons", {})
        
        # Extract data
        codon_names = list(codons.keys())
        frequencies = [codons[c]["frequency_percent"] for c in codon_names]
        counts = [codons[c]["count"] for c in codon_names]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.bar(codon_names, frequencies, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        
        # Add count labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{count:,}',
                   ha='center', va='bottom', fontsize=10)
        
        ax.set_xlabel('Stop Codon', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency (%)', fontsize=12, fontweight='bold')
        ax.set_title('Stop Codon Frequency Distribution', fontsize=14, fontweight='bold')
        ax.set_ylim(0, max(frequencies) * 1.2)
        
        plt.tight_layout()
        
        # Save
        if output_file is None:
            output_file = self.output_dir / "stop_codon_frequency.png"
        
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Stop codon chart saved to {output_file}")
        return str(output_file)
    
    def create_gene_length_histogram(self, gene_stats: Dict[str, Any], output_file: str = None) -> str:
        """
        Create histogram of gene lengths.
        
        Args:
            gene_stats: Gene statistics data
            output_file: Optional output file path
            
        Returns:
            Path to saved chart
        """
        # This would need actual gene length data
        # For now, create a placeholder based on stats
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        length_stats = gene_stats.get("length_stats", {})
        mean = length_stats.get("mean", 0)
        median = length_stats.get("median", 0)
        
        # Create sample data for visualization (in real implementation, use actual lengths)
        ax.axvline(mean, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean:.0f} bp')
        ax.axvline(median, color='blue', linestyle='--', linewidth=2, label=f'Median: {median:.0f} bp')
        
        ax.set_xlabel('Gene Length (bp)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title('Gene Length Distribution', fontsize=14, fontweight='bold')
        ax.legend()
        
        plt.tight_layout()
        
        if output_file is None:
            output_file = self.output_dir / "gene_length_histogram.png"
        
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Gene length histogram saved to {output_file}")
        return str(output_file)
    
    def create_nucleotide_composition_chart(self, composition: Dict[str, Any], output_file: str = None) -> str:
        """
        Create pie chart for nucleotide composition.
        
        Args:
            composition: Nucleotide composition data
            output_file: Optional output file path
            
        Returns:
            Path to saved chart
        """
        # Extract percentages
        nucleotides = ['A', 'T', 'G', 'C']
        percentages = [composition[n]["percentage"] for n in nucleotides]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        wedges, texts, autotexts = ax.pie(
            percentages,
            labels=nucleotides,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        
        # Enhance text
        for text in texts:
            text.set_fontsize(14)
            text.set_fontweight('bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
            autotext.set_fontweight('bold')
        
        ax.set_title('Nucleotide Composition', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if output_file is None:
            output_file = self.output_dir / "nucleotide_composition.png"
        
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Nucleotide composition chart saved to {output_file}")
        return str(output_file)
    
    def create_summary_dashboard(self, analysis_results: Dict[str, Any], output_file: str = None) -> str:
        """
        Create a summary dashboard with multiple charts.
        
        Args:
            analysis_results: Complete analysis results
            output_file: Optional output file path
            
        Returns:
            Path to saved dashboard
        """
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # Add charts here (implementation would add actual data)
        
        fig.suptitle('Genome Analysis Dashboard', fontsize=18, fontweight='bold')
        
        if output_file is None:
            output_file = self.output_dir / "analysis_dashboard.png"
        
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Analysis dashboard saved to {output_file}")
        return str(output_file)
