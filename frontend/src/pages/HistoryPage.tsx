import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
    Box,
    Typography,
    Card,
    CardContent,
    CardActions,
    Button,
    Grid,
    Chip,
    CircularProgress,
    Alert,
    LinearProgress,
} from '@mui/material'
import VisibilityIcon from '@mui/icons-material/Visibility'
import RefreshIcon from '@mui/icons-material/Refresh'
import { analysisService, AnalysisResponse } from '@/services/analysisService'

function HistoryPage() {
    const navigate = useNavigate()
    const [analyses, setAnalyses] = useState<AnalysisResponse[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        loadAnalyses()
    }, [])

    const loadAnalyses = async () => {
        try {
            setLoading(true)
            setError(null)
            const data = await analysisService.list(0, 100)
            setAnalyses(data)
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to load analyses')
        } finally {
            setLoading(false)
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
            case 'pending':
                return 'warning'
            default:
                return 'default'
        }
    }

    const viewResults = (analysisId: number) => {
        navigate(`/results/${analysisId}`)
    }

    const viewAnalysis = (analysisId: number) => {
        navigate(`/analysis/${analysisId}`)
    }

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
                <CircularProgress />
            </Box>
        )
    }

    return (
        <Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h4">
                    Analysis History
                </Typography>
                <Button
                    variant="outlined"
                    startIcon={<RefreshIcon />}
                    onClick={loadAnalyses}
                    disabled={loading}
                >
                    Refresh
                </Button>
            </Box>

            {error && (
                <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
                    {error}
                </Alert>
            )}

            {analyses.length === 0 && !loading && (
                <Box sx={{ textAlign: 'center', py: 8 }}>
                    <Typography variant="h6" color="text.secondary">
                        No analyses found
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        Start by searching for a genome and running an analysis
                    </Typography>
                    <Button
                        variant="contained"
                        sx={{ mt: 3 }}
                        onClick={() => navigate('/search')}
                    >
                        Search Genomes
                    </Button>
                </Box>
            )}

            <Grid container spacing={3}>
                {analyses.map((analysis) => (
                    <Grid item xs={12} key={analysis.id}>
                        <Card>
                            <CardContent>
                                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                                    <Box>
                                        <Typography variant="h6" gutterBottom>
                                            Analysis #{analysis.id}
                                        </Typography>
                                        <Typography variant="body2" color="text.secondary">
                                            Genome ID: {analysis.genome_id}
                                        </Typography>
                                    </Box>
                                    <Chip
                                        label={analysis.status.toUpperCase()}
                                        color={getStatusColor(analysis.status) as any}
                                    />
                                </Box>

                                {analysis.task_id && (
                                    <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1, fontFamily: 'monospace' }}>
                                        Task: {analysis.task_id}
                                    </Typography>
                                )}

                                {(analysis.status === 'running' || analysis.status === 'pending') && (
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
                                            sx={{ height: 6, borderRadius: 3 }}
                                        />
                                    </Box>
                                )}

                                <Grid container spacing={2}>
                                    <Grid item xs={12} sm={6}>
                                        <Typography variant="caption" color="text.secondary">
                                            Started At
                                        </Typography>
                                        <Typography variant="body2" fontWeight={500}>
                                            {new Date(analysis.started_at).toLocaleString()}
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
                                    {analysis.error_message && (
                                        <Grid item xs={12}>
                                            <Alert severity="error" sx={{ mt: 1 }}>
                                                {analysis.error_message}
                                            </Alert>
                                        </Grid>
                                    )}
                                </Grid>
                            </CardContent>

                            <CardActions sx={{ px: 2, pb: 2 }}>
                                {analysis.status === 'completed' && (
                                    <Button
                                        variant="contained"
                                        startIcon={<VisibilityIcon />}
                                        onClick={() => viewResults(analysis.id)}
                                    >
                                        View Results
                                    </Button>
                                )}
                                {(analysis.status === 'running' || analysis.status === 'pending') && (
                                    <Button
                                        variant="outlined"
                                        onClick={() => viewAnalysis(analysis.id)}
                                    >
                                        View Progress
                                    </Button>
                                )}
                            </CardActions>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </Box>
    )
}

export default HistoryPage
