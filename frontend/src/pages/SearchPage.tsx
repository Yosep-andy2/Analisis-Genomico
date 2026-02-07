import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import {
    Box,
    TextField,
    Button,
    Typography,
    Grid,
    Card,
    CardContent,
    CardActions,
    CircularProgress,
    Alert,
    Chip,
} from '@mui/material'
import SearchIcon from '@mui/icons-material/Search'
import BiotechIcon from '@mui/icons-material/Biotech'
import { genomesService, GenomeSearchResult } from '@/services/genomesService'
import { setSearchQuery, setSearchResults, setLoading, setError } from '@/store/slices/genomesSlice'
import { RootState } from '@/store'

function SearchPage() {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const { searchResults, loading, error, searchQuery } = useSelector((state: RootState) => state.genomes)
    const [query, setQuery] = useState(searchQuery || '')

    const handleSearch = async () => {
        if (!query.trim()) return

        dispatch(setLoading(true))
        dispatch(setSearchQuery(query))

        try {
            const results = await genomesService.search(query, 20)
            dispatch(setSearchResults(results))
        } catch (err: any) {
            dispatch(setError(err.response?.data?.detail || 'Failed to search genomes'))
        }
    }

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            handleSearch()
        }
    }

    const handleAnalyze = (accession: string) => {
        navigate(`/analysis/${accession}`)
    }

    const formatNumber = (num: number) => {
        return num.toLocaleString()
    }

    return (
        <Box>
            <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
                Search Genomes
            </Typography>

            <Box sx={{ mb: 4 }}>
                <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} md={9}>
                        <TextField
                            fullWidth
                            variant="outlined"
                            placeholder="Search by organism name or accession (e.g., Escherichia coli, NC_000913)"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            onKeyPress={handleKeyPress}
                            disabled={loading}
                        />
                    </Grid>
                    <Grid item xs={12} md={3}>
                        <Button
                            fullWidth
                            variant="contained"
                            size="large"
                            startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <SearchIcon />}
                            onClick={handleSearch}
                            disabled={loading || !query.trim()}
                            sx={{ height: 56 }}
                        >
                            {loading ? 'Searching...' : 'Search'}
                        </Button>
                    </Grid>
                </Grid>
            </Box>

            {error && (
                <Alert severity="error" sx={{ mb: 3 }} onClose={() => dispatch(setError(''))}>
                    {error}
                </Alert>
            )}

            {searchResults.length > 0 && (
                <Box>
                    <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
                        Found {searchResults.length} genome{searchResults.length !== 1 ? 's' : ''}
                    </Typography>

                    <Grid container spacing={3}>
                        {searchResults.map((genome: GenomeSearchResult) => (
                            <Grid item xs={12} key={genome.accession}>
                                <Card elevation={2}>
                                    <CardContent>
                                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                                            <Box sx={{ flex: 1 }}>
                                                <Typography variant="h6" gutterBottom>
                                                    {genome.organism}
                                                </Typography>
                                                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                                                    {genome.title}
                                                </Typography>
                                            </Box>
                                            <Chip
                                                label={genome.accession}
                                                color="primary"
                                                variant="outlined"
                                                sx={{ ml: 2 }}
                                            />
                                        </Box>

                                        <Grid container spacing={2}>
                                            <Grid item xs={12} sm={6} md={3}>
                                                <Typography variant="caption" color="text.secondary">
                                                    Length
                                                </Typography>
                                                <Typography variant="body1" fontWeight={500}>
                                                    {formatNumber(genome.length)} bp
                                                </Typography>
                                            </Grid>
                                            <Grid item xs={12} sm={6} md={3}>
                                                <Typography variant="caption" color="text.secondary">
                                                    Last Updated
                                                </Typography>
                                                <Typography variant="body1" fontWeight={500}>
                                                    {genome.update_date}
                                                </Typography>
                                            </Grid>
                                            {genome.gi && (
                                                <Grid item xs={12} sm={6} md={3}>
                                                    <Typography variant="caption" color="text.secondary">
                                                        GI Number
                                                    </Typography>
                                                    <Typography variant="body1" fontWeight={500}>
                                                        {genome.gi}
                                                    </Typography>
                                                </Grid>
                                            )}
                                        </Grid>
                                    </CardContent>

                                    <CardActions sx={{ px: 2, pb: 2 }}>
                                        <Button
                                            variant="contained"
                                            startIcon={<BiotechIcon />}
                                            onClick={() => handleAnalyze(genome.accession)}
                                        >
                                            Analyze Genome
                                        </Button>
                                    </CardActions>
                                </Card>
                            </Grid>
                        ))}
                    </Grid>
                </Box>
            )}

            {!loading && searchResults.length === 0 && searchQuery && (
                <Box sx={{ textAlign: 'center', py: 8 }}>
                    <Typography variant="h6" color="text.secondary">
                        No genomes found for "{searchQuery}"
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        Try searching with a different organism name or accession number
                    </Typography>
                </Box>
            )}

            {!loading && searchResults.length === 0 && !searchQuery && (
                <Box sx={{ textAlign: 'center', py: 8 }}>
                    <SearchIcon sx={{ fontSize: 80, color: 'text.disabled', mb: 2 }} />
                    <Typography variant="h6" color="text.secondary">
                        Search for genomes in NCBI GenBank
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        Enter an organism name or accession number to get started
                    </Typography>
                </Box>
            )}
        </Box>
    )
}

export default SearchPage
