"""Base analyzer class for genome analysis."""

from abc import ABC, abstractmethod
from typing import Dict, Any
from pathlib import Path


class BaseAnalyzer(ABC):
    """
    Abstract base class for genome analyzers.
    
    All analyzers should inherit from this class and implement
    the analyze method.
    """
    
    def __init__(self):
        """Initialize the analyzer."""
        self.results = {}
    
    @abstractmethod
    def analyze(self, genbank_file: str) -> Dict[str, Any]:
        """
        Analyze a GenBank file.
        
        Args:
            genbank_file: Path to GenBank file
            
        Returns:
            Dictionary with analysis results
        """
        pass
    
    def validate_file(self, genbank_file: str) -> bool:
        """
        Validate that the GenBank file exists.
        
        Args:
            genbank_file: Path to GenBank file
            
        Returns:
            True if file exists, False otherwise
        """
        return Path(genbank_file).exists()
