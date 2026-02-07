# Frontend

This is the frontend application for the Genomic Analysis Platform, built with React, TypeScript, and Material-UI.

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Material-UI v5** - Component library
- **Redux Toolkit** - State management
- **React Router v6** - Client-side routing
- **Axios** - HTTP client
- **Plotly.js** - Data visualization

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Start development server
npm run dev
```

The application will be available at http://localhost:3000

### Build for Production

```bash
npm run build
```

The production build will be in the `dist` directory.

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Layout.tsx      # Main layout wrapper
│   ├── Header.tsx      # Navigation header
│   └── Footer.tsx      # Footer component
├── pages/              # Page components
│   ├── HomePage.tsx    # Landing page
│   ├── SearchPage.tsx  # Genome search
│   ├── AnalysisPage.tsx # Analysis monitoring
│   ├── ResultsPage.tsx # Results display
│   └── HistoryPage.tsx # Analysis history
├── services/           # API services
│   ├── api.ts         # Axios client
│   ├── genomesService.ts
│   ├── analysisService.ts
│   └── resultsService.ts
├── store/             # Redux store
│   ├── index.ts       # Store configuration
│   └── slices/        # Redux slices
│       ├── genomesSlice.ts
│       └── analysisSlice.ts
├── App.tsx            # Main app component
├── main.tsx           # Entry point
├── theme.ts           # MUI theme
└── index.css          # Global styles
```

## Features

### 🔍 Genome Search
- Search genomes from NCBI GenBank
- Display search results with metadata
- Navigate to analysis

### 🧬 Analysis
- View genome details
- Start genome analysis
- Real-time progress tracking
- Automatic status polling

### 📊 Results
- Codon analysis (start/stop codons)
- Gene statistics
- Genome-wide metrics
- Validation against references
- Interactive data display

### 📜 History
- List all analyses
- View analysis status
- Navigate to results
- Refresh functionality

## API Integration

The frontend communicates with the backend API at `http://localhost:8000/api/v1` (configurable via `VITE_API_URL`).

### Endpoints Used

- `GET /genomes/search` - Search genomes
- `GET /genomes/{accession}` - Get genome details
- `POST /analysis/start` - Start analysis
- `GET /analysis/{id}` - Get analysis status
- `GET /analysis/` - List analyses
- `GET /results/{id}` - Get complete results

## State Management

Redux Toolkit is used for global state management:

- **genomesSlice**: Search query, results, loading states
- **analysisSlice**: Current analysis, analysis list, status

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

### Code Style

- TypeScript strict mode enabled
- ESLint for code quality
- Material-UI for consistent styling

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Troubleshooting

### API Connection Issues

If you get CORS errors or connection refused:

1. Make sure the backend is running at `http://localhost:8000`
2. Check the `VITE_API_URL` in your `.env` file
3. Verify the Vite proxy configuration in `vite.config.ts`

### Build Issues

If you encounter build errors:

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite
```

## License

This project is part of the Genomic Analysis Platform.
