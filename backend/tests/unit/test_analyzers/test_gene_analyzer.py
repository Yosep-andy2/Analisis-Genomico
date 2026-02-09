import pytest
import os
from app.analyzers.gene_analyzer import GeneAnalyzer

class TestGeneAnalyzer:
    def test_extract_genes(self, mock_genome_file):
        """Test gene extraction from the mock GenBank file."""
        analyzer = GeneAnalyzer()
        
        # Test basic extraction
        genes = analyzer.extract_genes(mock_genome_file)
        
        assert isinstance(genes, list)
        if len(genes) > 0:
            gene = genes[0]
            assert 'gene_name' in gene
            assert 'start' in gene
            assert 'end' in gene
            assert 'strand' in gene
            assert 'gc_content' in gene

    def test_calculate_statistics(self):
        """Test statistics calculation with dummy data."""
        analyzer = GeneAnalyzer()
        
        mock_genes = [
            {'length': 100, 'gc_content': 50.0},
            {'length': 200, 'gc_content': 60.0},
            {'length': 300, 'gc_content': 40.0}
        ]
        
        stats = analyzer.calculate_gene_statistics(mock_genes)
        
        assert stats['total_genes'] == 3
        assert stats['min_length'] == 100
        assert stats['max_length'] == 300
        assert stats['avg_length'] == 200.0
        assert stats['avg_gc_content'] == 50.0
