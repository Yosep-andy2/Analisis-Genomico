"""NCBI service for interacting with NCBI Entrez API."""

import time
from typing import List, Dict, Any, Optional
from pathlib import Path
from Bio import Entrez, SeqIO
import httpx
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import NCBIException, GenomeNotFoundException


class NCBIService:
    """
    Service for interacting with NCBI Entrez API.
    
    Provides:
    - Genome search
    - Genome download
    - Metadata retrieval
    """
    
    def __init__(self):
        """Initialize NCBI service."""
        # Configure Entrez
        Entrez.email = settings.NCBI_EMAIL
        if settings.NCBI_API_KEY:
            Entrez.api_key = settings.NCBI_API_KEY
        
        self.rate_limit = settings.NCBI_RATE_LIMIT
        self.last_request_time = 0
        self.download_dir = Path(settings.DATA_DIR) / "genomes"
        self.download_dir.mkdir(parents=True, exist_ok=True)
    
    def _rate_limit_wait(self):
        """Enforce rate limiting for NCBI API."""
        elapsed = time.time() - self.last_request_time
        min_interval = 1.0 / self.rate_limit
        
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        
        self.last_request_time = time.time()
    
    def search_genomes(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        Search for genomes in NCBI GenBank.
        
        Args:
            query: Search query (organism name or accession)
            max_results: Maximum number of results
            
        Returns:
            List of genome search results
        """
        logger.info(f"Searching NCBI for: {query}")
        
        try:
            self._rate_limit_wait()
            
            # Search nucleotide database
            search_handle = Entrez.esearch(
                db="nucleotide",
                term=f"{query}[Organism] AND complete genome[Title]",
                retmax=max_results,
                sort="relevance"
            )
            search_results = Entrez.read(search_handle)
            search_handle.close()
            
            id_list = search_results["IdList"]
            
            if not id_list:
                logger.info(f"No results found for query: {query}")
                return []
            
            # Fetch summaries
            self._rate_limit_wait()
            summary_handle = Entrez.esummary(db="nucleotide", id=",".join(id_list))
            summaries = Entrez.read(summary_handle)
            summary_handle.close()
            
            # Parse results
            results = []
            for summary in summaries:
                if isinstance(summary, dict):
                    result = {
                        "accession": summary.get("AccessionVersion", ""),
                        "title": summary.get("Title", ""),
                        "organism": self._extract_organism(summary.get("Title", "")),
                        "length": summary.get("Length", 0),
                        "update_date": summary.get("UpdateDate", ""),
                        "gi": summary.get("Gi", "")
                    }
                    results.append(result)
            
            logger.info(f"Found {len(results)} genomes")
            return results
            
        except Exception as e:
            logger.error(f"Error searching NCBI: {e}")
            raise NCBIException(f"Failed to search NCBI: {str(e)}")
    
    def download_genome(self, accession: str) -> str:
        """
        Download genome from NCBI GenBank.
        
        Args:
            accession: Genome accession number
            
        Returns:
            Path to downloaded GenBank file
        """
        logger.info(f"Downloading genome: {accession}")
        
        try:
            # Check if already downloaded
            output_file = self.download_dir / f"{accession}.gb"
            if output_file.exists():
                logger.info(f"Genome already downloaded: {output_file}")
                return str(output_file)
            
            self._rate_limit_wait()
            
            # Fetch GenBank record
            fetch_handle = Entrez.efetch(
                db="nucleotide",
                id=accession,
                rettype="gb",
                retmode="text"
            )
            
            # Save to file
            with open(output_file, 'w') as f:
                f.write(fetch_handle.read())
            
            fetch_handle.close()
            
            # Validate file
            if not self._validate_genbank_file(output_file):
                output_file.unlink()
                raise NCBIException(f"Downloaded file is not a valid GenBank file")
            
            logger.info(f"Genome downloaded successfully: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"Error downloading genome: {e}")
            raise NCBIException(f"Failed to download genome: {str(e)}")
    
    def get_genome_metadata(self, accession: str) -> Dict[str, Any]:
        """
        Get metadata for a genome.
        
        Args:
            accession: Genome accession number
            
        Returns:
            Genome metadata
        """
        logger.info(f"Fetching metadata for: {accession}")
        
        try:
            self._rate_limit_wait()
            
            # Fetch summary
            summary_handle = Entrez.esummary(db="nucleotide", id=accession)
            summaries = Entrez.read(summary_handle)
            summary_handle.close()
            
            if not summaries:
                raise GenomeNotFoundException(f"Genome not found: {accession}")
            
            summary = summaries[0]
            
            metadata = {
                "accession": summary.get("AccessionVersion", accession),
                "title": summary.get("Title", ""),
                "organism": self._extract_organism(summary.get("Title", "")),
                "length": summary.get("Length", 0),
                "create_date": summary.get("CreateDate", ""),
                "update_date": summary.get("UpdateDate", ""),
                "taxonomy": summary.get("TaxId", ""),
                "gi": summary.get("Gi", "")
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error fetching metadata: {e}")
            raise NCBIException(f"Failed to fetch metadata: {str(e)}")
    
    def _validate_genbank_file(self, file_path: Path) -> bool:
        """
        Validate that a file is a valid GenBank file.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if valid, False otherwise
        """
        try:
            record = SeqIO.read(str(file_path), "genbank")
            return len(record.seq) > 0
        except Exception as e:
            logger.error(f"GenBank validation failed: {e}")
            return False
    
    def _extract_organism(self, title: str) -> str:
        """
        Extract organism name from title.
        
        Args:
            title: GenBank title
            
        Returns:
            Organism name
        """
        # Simple extraction - take first part before comma
        parts = title.split(",")
        if parts:
            return parts[0].strip()
        return title
