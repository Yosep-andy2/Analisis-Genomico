import pytest
from unittest.mock import patch, MagicMock
from app.services.ncbi_service import NCBIService
from Bio import Entrez

class TestNCBIService:
    @patch('Bio.Entrez.esearch')
    def test_search_genomes(self, mock_esearch):
        """Test searching genomes with mocked Entrez."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.read.return_value = {
            "Count": "2",
            "RetMax": "2",
            "IdList": ["123", "456"],
            "TranslationSet": []
        }
        mock_esearch.return_value = mock_response
        
        service = NCBIService()
        
        # We need to mock esummary as well since search calls it to get details
        with patch('Bio.Entrez.esummary') as mock_esummary:
            mock_summary_response = MagicMock()
            mock_summary_response.read.return_value = {
                "DocumentSummarySet": {
                    "DocumentSummary": [
                        {
                            "AccessionVersion": "NC_000913.3",
                            "Title": "E. coli K-12",
                            "Organism": "Escherichia coli",
                            "Slen": 4600000,
                            "UpdateDate": "2024/01/01",
                            "Gi": "12345"
                        }
                    ]
                }
            }
            mock_esummary.return_value = mock_summary_response
            
            results = service.search_genomes("E. coli")
            
            assert len(results) > 0
            assert results[0]['accession'] == "NC_000913.3"
            assert results[0]['organism'] == "Escherichia coli"

    @patch('Bio.Entrez.efetch')
    def test_download_genome(self, mock_efetch, tmp_path):
        """Test genome download with mocked Entrez."""
        service = NCBIService()
        
        # Configure download path to tmp dir
        service.download_dir = str(tmp_path)
        
        # Mock file content
        mock_content = b"LOCUS..."
        mock_efetch.return_value = MagicMock(read=lambda: mock_content)
        
        file_path = service.download_genome("NC_000913.3")
        
        assert os.path.exists(file_path)
        assert file_path.endswith("NC_000913.3.gb")
