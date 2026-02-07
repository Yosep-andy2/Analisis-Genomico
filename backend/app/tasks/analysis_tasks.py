"""Analysis tasks for processing genomes."""

from celery import Task
from sqlalchemy.orm import Session
from app.tasks.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.analysis import Analysis
from app.models.result import Result
from app.models.validation import Validation
from app.analyzers.codon_analyzer import CodonAnalyzer
from app.analyzers.gene_analyzer import GeneAnalyzer
from app.analyzers.genome_analyzer import GenomeAnalyzer
from app.analyzers.visualization import VisualizationGenerator
from app.services.validation_service import ValidationService
from app.core.logging import logger
from app.core.exceptions import AnalysisException


class AnalysisTask(Task):
    """Base task for analysis with error handling."""
    
    autoretry_for = (AnalysisException,)
    retry_kwargs = {"max_retries": 2}
    retry_backoff = True


@celery_app.task(base=AnalysisTask, bind=True, name="analyze_genome")
def analyze_genome_task(self, analysis_id: int, genbank_file: str, accession: str) -> dict:
    """
    Perform complete genome analysis.
    
    Args:
        analysis_id: Database analysis ID
        genbank_file: Path to GenBank file
        accession: Genome accession number
        
    Returns:
        Dictionary with analysis results
    """
    logger.info(f"Task {self.request.id}: Starting analysis {analysis_id}")
    
    db: Session = SessionLocal()
    
    try:
        # Get analysis record
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            raise AnalysisException(f"Analysis {analysis_id} not found")
        
        # Update status
        analysis.status = "running"
        analysis.progress = 0.0
        analysis.message = "Starting analysis..."
        db.commit()
        
        # Step 1: Codon Analysis
        logger.info(f"Task {self.request.id}: Running codon analysis")
        analysis.progress = 10.0
        analysis.message = "Analyzing codons..."
        db.commit()
        
        codon_analyzer = CodonAnalyzer()
        codon_results = codon_analyzer.analyze(genbank_file)
        
        # Save codon results
        codon_result = Result(
            analysis_id=analysis_id,
            result_type="codon_analysis",
            data=codon_results
        )
        db.add(codon_result)
        db.commit()
        
        # Step 2: Gene Analysis
        logger.info(f"Task {self.request.id}: Running gene analysis")
        analysis.progress = 35.0
        analysis.message = "Analyzing genes..."
        db.commit()
        
        gene_analyzer = GeneAnalyzer()
        gene_results = gene_analyzer.analyze(genbank_file)
        
        # Save gene results
        gene_result = Result(
            analysis_id=analysis_id,
            result_type="gene_stats",
            data=gene_results
        )
        db.add(gene_result)
        db.commit()
        
        # Step 3: Genome Analysis
        logger.info(f"Task {self.request.id}: Running genome analysis")
        analysis.progress = 60.0
        analysis.message = "Analyzing genome statistics..."
        db.commit()
        
        genome_analyzer = GenomeAnalyzer()
        genome_results = genome_analyzer.analyze(genbank_file)
        
        # Save genome results
        genome_result = Result(
            analysis_id=analysis_id,
            result_type="genome_stats",
            data=genome_results
        )
        db.add(genome_result)
        db.commit()
        
        # Step 4: Validation
        logger.info(f"Task {self.request.id}: Running validation")
        analysis.progress = 80.0
        analysis.message = "Validating results..."
        db.commit()
        
        validation_service = ValidationService()
        validation_results = validation_service.validate_results(
            accession,
            {
                "codon_analysis": codon_results,
                "gene_stats": gene_results,
                "genome_stats": genome_results
            }
        )
        
        # Save validation
        validation = Validation(
            analysis_id=analysis_id,
            reference_accession=validation_results.get("reference_accession"),
            deviations=validation_results.get("validations"),
            validation_status=validation_results.get("status", "unknown")
        )
        db.add(validation)
        db.commit()
        
        # Step 5: Generate visualizations
        logger.info(f"Task {self.request.id}: Generating visualizations")
        analysis.progress = 90.0
        analysis.message = "Generating charts..."
        db.commit()
        
        viz_generator = VisualizationGenerator()
        charts = {}
        
        try:
            # Generate stop codon chart
            stop_codon_chart = viz_generator.create_stop_codon_chart(
                codon_results.get("stop_codons", {})
            )
            charts["stop_codon_frequency"] = stop_codon_chart
            
            # Generate nucleotide composition chart
            composition_chart = viz_generator.create_nucleotide_composition_chart(
                genome_results.get("nucleotide_composition", {})
            )
            charts["nucleotide_composition"] = composition_chart
            
        except Exception as e:
            logger.warning(f"Error generating charts: {e}")
        
        # Save chart paths
        if charts:
            chart_result = Result(
                analysis_id=analysis_id,
                result_type="charts",
                data=charts
            )
            db.add(chart_result)
            db.commit()
        
        # Mark as completed
        analysis.status = "completed"
        analysis.progress = 100.0
        analysis.message = "Analysis completed successfully"
        db.commit()
        
        logger.info(f"Task {self.request.id}: Analysis completed")
        
        return {
            "status": "completed",
            "analysis_id": analysis_id,
            "results": {
                "codon_analysis": codon_results,
                "gene_stats": gene_results,
                "genome_stats": genome_results,
                "validation": validation_results,
                "charts": charts
            }
        }
        
    except Exception as e:
        logger.error(f"Task {self.request.id}: Analysis failed - {e}")
        
        # Update analysis status
        if analysis:
            analysis.status = "failed"
            analysis.error_message = str(e)
            analysis.message = "Analysis failed"
            db.commit()
        
        raise
        
    finally:
        db.close()
