import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import {
    Box,
    Typography,
    Button,
    Card,
    CardContent,
    LinearProgress,
    Alert,
    Chip,
    Grid,
    Paper,
    CircularProgress,
} from '@mui/material'
import PlayArrowIcon from '@mui/icons-material/PlayArrow'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import ErrorIcon from '@mui/icons-material/Error'
import VisibilityIcon from '@mui/icons-material/Visibility'
import { genomesService } from '@/services/genomesService'
import { analysisService, AnalysisStatus } from '@/services/analysisService'
import { setCurrentAnalysis } from '@/store/slices/analysisSlice'

function AnalysisPage() {
    const { accession } = useParams<{ accession: string }>()
    const navigate = useNavigate()
    const dispatch = useDispatch()

    const [genomeDetails, setGenomeDetails] = useState<any>(null)
    const [analysis, setAnalysis] = useState<AnalysisStatus | null>(null)
    const [loading, setLoading] = useState(true)
    const [starting, setStarting] = useState(false)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        loadGenomeDetails()
    }, [accession])

    useEffect(() => {
        if (analysis && analysis.status !== 'completed' && analysis.status !== 'failed') {
            const interval = setInterval(() => {
                pollAnalysisStatus()
            }, 3000) // Poll every 3 seconds

            return () => clearInterval(interval)
        }
    }, [analysis])

    const loadGenomeDetails = async () => {
        if (!accession) return

        try {
            setLoading(true)
            const details = await genomesService.getDetails(accession)
            setGenomeDetails(details)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to load genome details')
        } finally {
            setLoading(false)
        }
    }

    const startAnalysis = async () => {
        if (!accession) return

        try {
            setStarting(true)
            setError(null)
            const result = await analysisService.start(accession)
            setAnalysis(result)
            dispatch(setCurrentAnalysis(result))
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to start analysis')
        } finally {
            setStarting(false)
        }
    }

    const pollAnalysisStatus = async () => {
        if (!analysis) return

        try {
            const status = await analysisService.getStatus(analysis.analysis_id)
            setAnalysis(status)
            dispatch(setCurrentAnalysis(status))
        } catch (err) {
            console.error('Failed to poll analysis status:', err)
        }
    }

    const viewResults = () => {
        if (analysis) {
            navigate(`/results/${analysis.analysis_id}`)
        }
    }

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'completed':
                return 'success'
            case 'failed':
                return 'error'
            case 'running':
                return 'primary'
            default:
                return 'default'
        }
    }

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'completed':
                return <CheckCircleIcon />
            case 'failed':
                return <ErrorIcon />
            default:
                return null
        }
    }

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
                <CircularProgress />
            </Box>
        )
    }

    if (error && !genomeDetails) {
        return (
            <Alert severity="error" sx={{ mb: 3 }}>
                {error}
            </Alert>
        )
    }

    return (
        <Box>
            <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
                Genome Analysis
            </Typography>

            {genomeDetails && (
                <Card sx={{ mb: 3 }}>
                    <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                            <Box>
                                <Typography variant="h5" gutterBottom>
                                    {genomeDetails.organism}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                    {genomeDetails.title}
                                </Typography>
                            </Box>
                            <Chip label={genomeDetails.accession} color="primary" />
                        </Box>

                        <Grid container spacing={2} sx={{ mt: 2 }}>
                            <Grid item xs={12} sm={6} md={3}>
                                <Typography variant="caption" color="text.secondary">
                                    Length
                                </Typography>
                                <Typography variant="body1" fontWeight={500}>
                                    {genomeDetails.length.toLocaleString()} bp
                                </Typography>
                            </Grid>
                            <Grid item xs={12} sm={6} md={3}>
                                <Typography variant="caption" color="text.secondary">
                                    Created
                                </Typography>
                                <Typography variant="body1" fontWeight={500}>
                                    {genomeDetails.create_date}
                                </Typography>
                            </Grid>
                            <Grid item xs={12} sm={6} md={3}>
                                <Typography variant="caption" color="text.secondary">
                                    Updated
                                </Typography>
                                <Typography variant="body1" fontWeight={500}>
                                    {genomeDetails.update_date}
                                </Typography>
                            </Grid>
                            <Grid item xs={12} sm={6} md={3}>
                                <Typography variant="caption" color="text.secondary">
                                    Taxonomy ID
                                </Typography>
                                <Typography variant="body1" fontWeight={500}>
                                    {genomeDetails.taxonomy}
                                </Typography>
                            </Grid>
                        </Grid>
                    </CardContent>
                </Card>
            )}

            {error && (
                <Alert severity="error" sx={{ mb: 3 }}>
                    {error}
                </Alert>
            )}

            {!analysis && (
                <Paper sx={{ p: 4, textAlign: 'center' }}>
                    <Typography variant="h6" gutterBottom>
                        Ready to analyze this genome
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                        The analysis will include codon analysis, gene statistics, genome-wide metrics, and validation
                    </Typography>
                    <Button
                        variant="contained"
                        size="large"
                        startIcon={starting ? <CircularProgress size={20} color="inherit" /> : <PlayArrowIcon />}
                        onClick={startAnalysis}
                        disabled={starting}
                    >
                        {starting ? 'Starting Analysis...' : 'Start Analysis'}
                    </Button>
                </Paper>
            )}

            {analysis && (
                <Card>
                    <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                            <Typography variant="h6">
                                Analysis Status
                            </Typography>
                            <Chip
                                label={analysis.status.toUpperCase()}
                                color={getStatusColor(analysis.status)}
                                icon={getStatusIcon(analysis.status) || undefined}
                            />
                        </Box>

                        {analysis.message && (
                            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                                {analysis.message}
                            </Typography>
                        )}

                        <Box sx={{ mb: 2 }}>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                <Typography variant="body2" color="text.secondary">
                                    Progress
                                </Typography>
                                <Typography variant="body2" fontWeight={500}>
                                    {Math.round(analysis.progress)}%
                                </Typography>
                            </Box>
                            <LinearProgress
                                variant="determinate"
                                value={analysis.progress}
                                sx={{ height: 8, borderRadius: 4 }}
                            />
                        </Box>

                        <Grid container spacing={2}>
                            <Grid item xs={12} sm={6}>
                                <Typography variant="caption" color="text.secondary">
                                    Analysis ID
                                </Typography>
                                <Typography variant="body2" fontWeight={500}>
                                    {analysis.analysis_id}
                                </Typography>
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <Typography variant="caption" color="text.secondary">
                                    Task ID
                                </Typography>
                                <Typography variant="body2" fontWeight={500} sx={{ fontFamily: 'monospace', fontSize: '0.75rem' }}>
                                    {analysis.task_id}
                                </Typography>
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <Typography variant="caption" color="text.secondary">
                                    Started At
                                </Typography>
                                <Typography variant="body2" fontWeight={500}>
                                    {analysis.started_at ? new Date(analysis.started_at).toLocaleString() : 'N/A'}
                                </Typography>
                            </Grid>
                            {analysis.completed_at && (
                                <Grid item xs={12} sm={6}>
                                    <Typography variant="caption" color="text.secondary">
                                        Completed At
                                    </Typography>
                                    <Typography variant="body2" fontWeight={500}>
                                        {new Date(analysis.completed_at).toLocaleString()}
                                    </Typography>
                                </Grid>
                            )}
                        </Grid>

                        {analysis.status === 'completed' && (
                            <Box sx={{ mt: 3, textAlign: 'center' }}>
                                <Button
                                    variant="contained"
                                    size="large"
                                    startIcon={<VisibilityIcon />}
                                    onClick={viewResults}
                                >
                                    View Results
                                </Button>
                            </Box>
                        )}
                    </CardContent>
                </Card>
            )}
        </Box>
    )
}

export default AnalysisPage
