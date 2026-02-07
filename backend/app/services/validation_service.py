"""Validation service for comparing results with reference genomes."""

import json
from typing import Dict, Any, Optional
from pathlib import Path
from app.core.logging import logger


class ValidationService:
    """
    Service for validating analysis results against reference genomes.
    
    Compares:
    - Genome size
    - GC content
    - Gene count
    - Stop codon frequencies
    """
    
    def __init__(self, reference_file: str = "./data/reference/reference_genomes.json"):
        """
        Initialize validation service.
        
        Args:
            reference_file: Path to reference genomes JSON file
        """
        self.reference_file = Path(reference_file)
        self.references = self._load_references()
    
    def _load_references(self) -> Dict[str, Any]:
        """
        Load reference genome data from JSON file.
        
        Returns:
            Dictionary of reference genomes
        """
        if not self.reference_file.exists():
            logger.warning(f"Reference file not found: {self.reference_file}")
            return {}
        
        try:
            with open(self.reference_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading reference file: {e}")
            return {}
    
    def validate_results(self, accession: str, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate analysis results against reference genome.
        
        Args:
            accession: Genome accession number
            results: Analysis results to validate
            
        Returns:
            Validation report with deviations
        """
        # Get reference data
        reference = self.references.get(accession)
        
        if not reference:
            return {
                "status": "no_reference",
                "message": f"No reference data available for {accession}",
                "validated": False
            }
        
        logger.info(f"Validating results against reference: {accession}")
        
        # Extract data from results
        genome_stats = results.get("genome_stats", {})
        gene_stats = results.get("gene_stats", {}).get("statistics", {})
        stop_codons = results.get("codon_analysis", {}).get("stop_codons", {}).get("codons", {})
        
        # Validate each metric
        validations = {}
        
        # Genome size
        if "genome_size" in genome_stats:
            validations["genome_size"] = self._validate_metric(
                "Genome Size",
                genome_stats["genome_size"],
                reference["genome_size"],
                tolerance_percent=1.0
            )
        
        # GC content
        if "gc_content" in genome_stats:
            validations["gc_content"] = self._validate_metric(
                "GC Content",
                genome_stats["gc_content"],
                reference["gc_content"],
                tolerance_percent=0.5
            )
        
        # Gene count
        if "total_genes" in gene_stats:
            validations["gene_count"] = self._validate_metric(
                "Gene Count",
                gene_stats["total_genes"],
                reference["gene_count"],
                tolerance_percent=5.0
            )
        
        # Average gene length
        if "length_stats" in gene_stats:
            avg_length = gene_stats["length_stats"].get("mean", 0)
            validations["avg_gene_length"] = self._validate_metric(
                "Average Gene Length",
                avg_length,
                reference.get("avg_gene_length", 0),
                tolerance_percent=10.0
            )
        
        # Stop codon frequencies
        if stop_codons:
            ref_stop_freqs = reference.get("stop_codon_frequencies", {})
            for codon in ["TAA", "TAG", "TGA"]:
                if codon in stop_codons and codon in ref_stop_freqs:
                    observed_freq = stop_codons[codon]["frequency_percent"] / 100
                    expected_freq = ref_stop_freqs[codon]
                    
                    validations[f"stop_codon_{codon}"] = self._validate_metric(
                        f"Stop Codon {codon} Frequency",
                        observed_freq,
                        expected_freq,
                        tolerance_percent=5.0
                    )
        
        # Determine overall status
        overall_status = self._determine_overall_status(validations)
        
        return {
            "status": overall_status,
            "reference_accession": accession,
            "reference_organism": reference.get("organism", "Unknown"),
            "validations": validations,
            "validated": True,
            "reference_citation": reference.get("reference", "")
        }
    
    def _validate_metric(
        self,
        name: str,
        observed: float,
        expected: float,
        tolerance_percent: float = 5.0
    ) -> Dict[str, Any]:
        """
        Validate a single metric against expected value.
        
        Args:
            name: Metric name
            observed: Observed value
            expected: Expected value
            tolerance_percent: Tolerance percentage
            
        Returns:
            Validation result
        """
        if expected == 0:
            deviation_percent = 0
        else:
            deviation_percent = abs((observed - expected) / expected * 100)
        
        passed = deviation_percent <= tolerance_percent
        
        if passed:
            status = "passed"
        elif deviation_percent <= tolerance_percent * 2:
            status = "warning"
        else:
            status = "failed"
        
        return {
            "metric": name,
            "observed": round(observed, 2),
            "expected": round(expected, 2),
            "deviation_percent": round(deviation_percent, 2),
            "tolerance_percent": tolerance_percent,
            "status": status,
            "passed": passed
        }
    
    def _determine_overall_status(self, validations: Dict[str, Any]) -> str:
        """
        Determine overall validation status.
        
        Args:
            validations: Dictionary of validation results
            
        Returns:
            Overall status (passed, warning, failed)
        """
        if not validations:
            return "unknown"
        
        statuses = [v["status"] for v in validations.values()]
        
        if "failed" in statuses:
            return "failed"
        elif "warning" in statuses:
            return "warning"
        else:
            return "passed"
    
    def get_reference_info(self, accession: str) -> Optional[Dict[str, Any]]:
        """
        Get reference genome information.
        
        Args:
            accession: Genome accession number
            
        Returns:
            Reference genome data or None
        """
        return self.references.get(accession)
    
    def list_available_references(self) -> list:
        """
        List all available reference genomes.
        
        Returns:
            List of accession numbers
        """
        return list(self.references.keys())
