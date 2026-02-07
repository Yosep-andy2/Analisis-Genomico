import { Box, Container, Typography, Link } from '@mui/material'

function Footer() {
    return (
        <Box
            component="footer"
            sx={{
                py: 3,
                px: 2,
                mt: 'auto',
                backgroundColor: (theme) => theme.palette.grey[200],
            }}
        >
            <Container maxWidth="xl">
                <Typography variant="body2" color="text.secondary" align="center">
                    {'Genomic Analysis Platform © '}
                    {new Date().getFullYear()}
                    {' | Built with '}
                    <Link color="inherit" href="https://biopython.org/" target="_blank" rel="noopener">
                        BioPython
                    </Link>
                    {' and '}
                    <Link color="inherit" href="https://www.ncbi.nlm.nih.gov/" target="_blank" rel="noopener">
                        NCBI
                    </Link>
                </Typography>
            </Container>
        </Box>
    )
}

export default Footer
