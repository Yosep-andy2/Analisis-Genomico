import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import {
    Box,
    Typography,
    Card,
    CardContent,
    Grid,
    Chip,
    CircularProgress,
    Alert,
    Paper,
    Divider,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Accordion,
    AccordionSummary,
    AccordionDetails,
} from '@mui/material'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import WarningIcon from '@mui/icons-material/Warning'
import ErrorIcon from '@mui/icons-material/Error'
import { resultsService, CompleteAnalysisResult } from '@/services/resultsService'

function ResultsPage() {
    const { analysisId } = useParams<{ analysisId: string }>()
    const [results, setResults] = useState<CompleteAnalysisResult | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        loadResults()
    }, [analysisId])

    const loadResults = async () => {
        if (!analysisId) return

        try {
            setLoading(true)
            const data = await resultsService.getComplete(parseInt(analysisId))
            setResults(data)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to load results')
        } finally {
            setLoading(false)
        }
    }

    const getValidationIcon = (status: string) => {
        switch (status) {
            case 'passed':
                return <CheckCircleIcon color="success" />
            case 'warning':
                return <WarningIcon color="warning" />
            case 'failed':
                return <ErrorIcon color="error" />
            default:
                return null
        }
    }

    const getValidationColor = (status: string) => {
        switch (status) {
            case 'passed':
                return 'success'
            case 'warning':
                return 'warning'
            case 'failed':
                return 'error'
            default:
                return 'default'
        }
    }

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
                <CircularProgress />
            </Box>
        )
    }

    if (error || !results) {
        return (
            <Alert severity="error">
                {error || 'Results not found'}
            </Alert>
        )
    }

    return (
        <Box>
            <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
                Analysis Results
            </Typography>

            {/* Header Info */}
            <Card sx={{ mb: 3 }}>
                <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                        <Box>
                            <Typography variant="h5" gutterBottom>
                                {results.organism}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                                Analysis ID: {results.analysis_id}
                            </Typography>
                        </Box>
                        <Chip label={results.genome_accession} color="primary" />
                    </Box>
                </CardContent>
            </Card>

            {/* Codon Analysis */}
            {results.codon_analysis && (
                <Accordion defaultExpanded>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Typography variant="h6">🧬 Codon Analysis</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Grid container spacing={3}>
                            {/* Start Codons */}
                            <Grid item xs={12} md={6}>
                                <Paper sx={{ p: 2 }}>
                                    <Typography variant="subtitle1" gutterBottom fontWeight={600}>
                                        Start Codons (ATG)
                                    </Typography>
                                    <Divider sx={{ my: 1 }} />
                                    <Grid container spacing={2}>
                                        <Grid item xs={6}>
                                            <Typography variant="caption" color="text.secondary">
                                                Total Count
                                            </Typography>
                                            <Typography variant="h6">
                                                {results.codon_analysis.start_codons?.total_count?.toLocaleString() || 0}
                                            </Typography>
                                        </Grid>
                                        <Grid item xs={6}>
                                            <Typography variant="caption" color="text.secondary">
                                                Density (per kb)
                                            </Typography>
                                            <Typography variant="h6">
                                                {results.codon_analysis.start_codons?.density_per_kb?.toFixed(2) || 0}
                                            </Typography>
                                        </Grid>
                                    </Grid>
                                </Paper>
                            </Grid>

                            {/* Stop Codons */}
                            <Grid item xs={12} md={6}>
                                <Paper sx={{ p: 2 }}>
                                    <Typography variant="subtitle1" gutterBottom fontWeight={600}>
                                        Stop Codons
                                    </Typography>
                                    <Divider sx={{ my: 1 }} />
                                    <Grid container spacing={2}>
                                        <Grid item xs={4}>
                                            <Typography variant="caption" color="text.secondary">
                                                TAA
                                            </Typography>
                                            <Typography variant="h6">
                                                {results.codon_analysis.stop_codons?.TAA || 0}
                                            </Typography>
                                        </Grid>
                                        <Grid item xs={4}>
                                            <Typography variant="caption" color="text.secondary">
                                                TAG
                                            </Typography>
                                            <Typography variant="h6">
                                                {results.codon_analysis.stop_codons?.TAG || 0}
                                            </Typography>
                                        </Grid>
                                        <Grid item xs={4}>
                                            <Typography variant="caption" color="text.secondary">
                                                TGA
                                            </Typography>
                                            <Typography variant="h6">
                                                {results.codon_analysis.stop_codons?.TGA || 0}
                                            </Typography>
                                        </Grid>
                                    </Grid>
                                </Paper>
                            </Grid>
                        </Grid>
                    </AccordionDetails>
                </Accordion>
            )}

            {/* Gene Statistics */}
            {results.gene_stats && (
                <Accordion defaultExpanded>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Typography variant="h6">📊 Gene Statistics</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Grid container spacing={3}>
                            <Grid item xs={12} sm={6} md={3}>
                                <Paper sx={{ p: 2, textAlign: 'center' }}>
                                    <Typography variant="caption" color="text.secondary">
                                        Total Genes
                                    </Typography>
                                    <Typography variant="h4" color="primary">
                                        {results.gene_stats.total_genes || 0}
                                    </Typography>
                                </Paper>
                            </Grid>
                            <Grid item xs={12} sm={6} md={3}>
                                <Paper sx={{ p: 2, textAlign: 'center' }}>
                                    <Typography variant="caption" color="text.secondary">
                                        Avg Length (bp)
                                    </Typography>
                                    <Typography variant="h4" color="primary">
                                        {results.gene_stats.length_stats?.mean?.toFixed(0) || 0}
                                    </Typography>
                                </Paper>
                            </Grid>
                            <Grid item xs={12} sm={6} md={3}>
                                <Paper sx={{ p: 2, textAlign: 'center' }}>
                                    <Typography variant="caption" color="text.secondary">
                                        Avg GC Content
                                    </Typography>
                                    <Typography variant="h4" color="primary">
                                        {results.gene_stats.gc_content_stats?.mean?.toFixed(1) || 0}%
                                    </Typography>
                                </Paper>
                            </Grid>
                            <Grid item xs={12} sm={6} md={3}>
                                <Paper sx={{ p: 2, textAlign: 'center' }}>
                                    <Typography variant="caption" color="text.secondary">
                                        Forward Strand
                                    </Typography>
                                    <Typography variant="h4" color="primary">
                                        {results.gene_stats.strand_distribution?.forward || 0}
                                    </Typography>
                                </Paper>
                            </Grid>
                        </Grid>
                    </AccordionDetails>
                </Accordion>
            )}

            {/* Genome Statistics */}
            {results.genome_stats && (
                <Accordion defaultExpanded>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Typography variant="h6">🌐 Genome Statistics</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Grid container spacing={3}>
                            <Grid item xs={12} sm={6} md={3}>
                                <Paper sx={{ p: 2, textAlign: 'center' }}>
                                    <Typography variant="caption" color="text.secondary">
                                        Genome Size
                                    </Typography>
                                    <Typography variant="h5" color="primary">
                                        {results.genome_stats.genome_size?.toLocaleString() || 0} bp
                                    </Typography>
                                </Paper>
                            </Grid>
                            <Grid item xs={12} sm={6} md={3}>
                                <Paper sx={{ p: 2, textAlign: 'center' }}>
                                    <Typography variant="caption" color="text.secondary">
                                        GC Content
                                    </Typography>
                                    <Typography variant="h5" color="primary">
                                        {results.genome_stats.gc_content?.toFixed(2) || 0}%
                                    </Typography>
                                </Paper>
                            </Grid>
                            <Grid item xs={12} sm={6} md={3}>
                                <Paper sx={{ p: 2, textAlign: 'center' }}>
                                    <Typography variant="caption" color="text.secondary">
                                        Coding Density
                                    </Typography>
                                    <Typography variant="h5" color="primary">
                                        {results.genome_stats.coding_density?.toFixed(2) || 0}%
                                    </Typography>
                                </Paper>
                            </Grid>
                            <Grid item xs={12} sm={6} md={3}>
                                <Paper sx={{ p: 2, textAlign: 'center' }}>
                                    <Typography variant="caption" color="text.secondary">
                                        AT Content
                                    </Typography>
                                    <Typography variant="h5" color="primary">
                                        {((results.genome_stats.nucleotide_composition?.A || 0) +
                                            (results.genome_stats.nucleotide_composition?.T || 0)).toFixed(2)}%
                                    </Typography>
                                </Paper>
                            </Grid>
                        </Grid>

                        {results.genome_stats.nucleotide_composition && (
                            <Box sx={{ mt: 3 }}>
                                <Typography variant="subtitle2" gutterBottom>
                                    Nucleotide Composition
                                </Typography>
                                <TableContainer component={Paper} variant="outlined">
                                    <Table size="small">
                                        <TableHead>
                                            <TableRow>
                                                <TableCell>Nucleotide</TableCell>
                                                <TableCell align="right">Percentage</TableCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {Object.entries(results.genome_stats.nucleotide_composition).map(([base, percentage]) => (
                                                <TableRow key={base}>
                                                    <TableCell component="th" scope="row">
                                                        <strong>{base}</strong>
                                                    </TableCell>
                                                    <TableCell align="right">{(percentage as number).toFixed(2)}%</TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            </Box>
                        )}
                    </AccordionDetails>
                </Accordion>
            )}

            {/* Validation */}
            {results.validation && (
                <Accordion defaultExpanded>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="h6">✅ Validation</Typography>
                            {getValidationIcon(results.validation.status)}
                        </Box>
                    </AccordionSummary>
                    <AccordionDetails>
                        <Box sx={{ mb: 2 }}>
                            <Chip
                                label={`Status: ${results.validation.status.toUpperCase()}`}
                                color={getValidationColor(results.validation.status) as any}
                                sx={{ mr: 1 }}
                            />
                            {results.validation.reference_accession && (
                                <Chip
                                    label={`Reference: ${results.validation.reference_accession}`}
                                    variant="outlined"
                                />
                            )}
                        </Box>

                        {results.validation.validations && Object.keys(results.validation.validations).length > 0 && (
                            <TableContainer component={Paper} variant="outlined">
                                <Table size="small">
                                    <TableHead>
                                        <TableRow>
                                            <TableCell>Metric</TableCell>
                                            <TableCell align="right">Status</TableCell>
                                            <TableCell align="right">Details</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {Object.entries(results.validation.validations).map(([metric, data]: [string, any]) => (
                                            <TableRow key={metric}>
                                                <TableCell component="th" scope="row">
                                                    {metric.replace(/_/g, ' ').toUpperCase()}
                                                </TableCell>
                                                <TableCell align="right">
                                                    <Chip
                                                        label={data.status}
                                                        size="small"
                                                        color={getValidationColor(data.status) as any}
                                                    />
                                                </TableCell>
                                                <TableCell align="right">
                                                    <Typography variant="caption">
                                                        {data.message || 'N/A'}
                                                    </Typography>
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        )}
                    </AccordionDetails>
                </Accordion>
            )}
        </Box>
    )
}

export default ResultsPage
