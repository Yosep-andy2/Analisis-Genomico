import { Box, Typography, Button, Container, Paper } from '@mui/material'
import { useNavigate } from 'react-router-dom'
import SearchIcon from '@mui/icons-material/Search'
import BiotechIcon from '@mui/icons-material/Biotech'

function HomePage() {
    const navigate = useNavigate()

    return (
        <Container maxWidth="md">
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    textAlign: 'center',
                    py: 8,
                }}
            >
                <BiotechIcon sx={{ fontSize: 80, color: 'primary.main', mb: 3 }} />

                <Typography variant="h2" component="h1" gutterBottom>
                    Genomic Analysis Platform
                </Typography>

                <Typography variant="h5" color="text.secondary" paragraph sx={{ mb: 4 }}>
                    Automated genome analysis with NCBI integration
                </Typography>

                <Paper elevation={3} sx={{ p: 4, width: '100%', mb: 4 }}>
                    <Typography variant="h6" gutterBottom>
                        Features
                    </Typography>
                    <Box sx={{ textAlign: 'left', mt: 2 }}>
                        <Typography variant="body1" paragraph>
                            🧬 <strong>Genome Search:</strong> Search and download genomes from NCBI GenBank
                        </Typography>
                        <Typography variant="body1" paragraph>
                            🔬 <strong>Automated Analysis:</strong> Codon analysis, gene statistics, and genome-wide metrics
                        </Typography>
                        <Typography variant="body1" paragraph>
                            ✅ <strong>Validation:</strong> Compare results against reference genomes
                        </Typography>
                        <Typography variant="body1" paragraph>
                            📊 <strong>Visualization:</strong> Professional charts and interactive plots
                        </Typography>
                        <Typography variant="body1" paragraph>
                            💾 <strong>Export:</strong> Download results in JSON, CSV, and PDF formats
                        </Typography>
                    </Box>
                </Paper>

                <Button
                    variant="contained"
                    size="large"
                    startIcon={<SearchIcon />}
                    onClick={() => navigate('/search')}
                    sx={{ px: 4, py: 1.5 }}
                >
                    Start Searching Genomes
                </Button>
            </Box>
        </Container>
    )
}

export default HomePage
