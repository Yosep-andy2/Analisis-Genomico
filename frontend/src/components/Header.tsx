import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material'
import { Link as RouterLink } from 'react-router-dom'
import BiotechIcon from '@mui/icons-material/Biotech'
import SearchIcon from '@mui/icons-material/Search'
import HistoryIcon from '@mui/icons-material/History'

function Header() {
    return (
        <AppBar position="static" elevation={2}>
            <Toolbar>
                <BiotechIcon sx={{ mr: 2 }} />
                <Typography
                    variant="h6"
                    component={RouterLink}
                    to="/"
                    sx={{
                        flexGrow: 1,
                        textDecoration: 'none',
                        color: 'inherit',
                        fontWeight: 600,
                    }}
                >
                    Genomic Analysis Platform
                </Typography>

                <Box sx={{ display: 'flex', gap: 2 }}>
                    <Button
                        color="inherit"
                        component={RouterLink}
                        to="/search"
                        startIcon={<SearchIcon />}
                    >
                        Search
                    </Button>
                    <Button
                        color="inherit"
                        component={RouterLink}
                        to="/history"
                        startIcon={<HistoryIcon />}
                    >
                        History
                    </Button>
                </Box>
            </Toolbar>
        </AppBar>
    )
}

export default Header
