import pytest
from app.analyzers.codon_analyzer import CodonAnalyzer

class TestCodonAnalyzer:
    def test_count_start_codons(self):
        analyzer = CodonAnalyzer()
        # Sequence with 2 initial ATGs (case insensitive test)
        sequence = "ATGccctttATGaaa"
        
        result = analyzer.count_start_codons(sequence)
        
        assert result['total_count'] == 2
        assert result['positions'] == [0, 9]
        assert result['density_per_kb'] > 0

    def test_count_stop_codons(self):
        analyzer = CodonAnalyzer()
        # Sequence with TAA, TAG, TGA
        sequence = "ccTAAaccTAGcccTGA"
        
        result = analyzer.count_stop_codons(sequence)
        
        assert result['stop_codons']['TAA'] == 1
        assert result['stop_codons']['TAG'] == 1
        assert result['stop_codons']['TGA'] == 1
        assert result['stop_codons']['total'] == 3

    def test_empty_sequence(self):
        analyzer = CodonAnalyzer()
        result = analyzer.count_start_codons("")
        assert result['total_count'] == 0
        
        result = analyzer.count_stop_codons("")
        assert result['stop_codons']['total'] == 0
