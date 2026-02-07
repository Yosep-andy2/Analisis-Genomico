"""Custom exceptions for the application."""


class GenomicsException(Exception):
    """Base exception for genomics application."""
    pass


class NCBIException(GenomicsException):
    """Exception raised for NCBI API errors."""
    pass


class GenomeNotFoundException(GenomicsException):
    """Exception raised when genome is not found."""
    pass


class AnalysisException(GenomicsException):
    """Exception raised during genome analysis."""
    pass


class ValidationException(GenomicsException):
    """Exception raised during result validation."""
    pass


class FileSizeException(GenomicsException):
    """Exception raised when file size exceeds limit."""
    pass
