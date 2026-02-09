import pytest
from app.analyzers.genome_analyzer import GenomeAnalyzer

class TestGenomeAnalyzer:
    def test_calculate_statistics(self, mock_genome_file):
        """Test genome statistics calculation."""
        analyzer = GenomeAnalyzer()
        
        stats = analyzer.calculate_statistics(mock_genome_file)
        
        # Check basic stats presence
        assert 'genome_size' in stats
        assert 'gc_content' in stats
        assert 'nucleotide_composition' in stats
        
        # Check values from mock file
        # Mock file has ~300bp (it's small)
        assert stats['genome_size'] > 0
        
        # Check nucleotide composition
        comp = stats['nucleotide_composition']
        assert 'A' in comp
        assert 'C' in comp
        assert 'G' in comp
        assert 'T' in comp
        
        # Percentages should sum to roughly 100
        total_pct = sum(comp.values())
        assert 99.0 <= total_pct <= 101.0

    def test_coding_density(self, mock_genome_file):
        """Test coding density calculation."""
        analyzer = GenomeAnalyzer()
        
        # Mock file has one CDS defined
        density = analyzer.calculate_coding_density(mock_genome_file)
        
        assert isinstance(density, float)
        assert 0.0 <= density <= 100.0
