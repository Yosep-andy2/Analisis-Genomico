import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface GenomeSearchResult {
    accession: string
    title: string
    organism: string
    length: number
    update_date: string
    gi?: string
}

interface GenomesState {
    searchResults: GenomeSearchResult[]
    loading: boolean
    error: string | null
    searchQuery: string
}

const initialState: GenomesState = {
    searchResults: [],
    loading: false,
    error: null,
    searchQuery: '',
}

const genomesSlice = createSlice({
    name: 'genomes',
    initialState,
    reducers: {
        setSearchQuery: (state, action: PayloadAction<string>) => {
            state.searchQuery = action.payload
        },
        setSearchResults: (state, action: PayloadAction<GenomeSearchResult[]>) => {
            state.searchResults = action.payload
            state.loading = false
            state.error = null
        },
        setLoading: (state, action: PayloadAction<boolean>) => {
            state.loading = action.payload
        },
        setError: (state, action: PayloadAction<string>) => {
            state.error = action.payload
            state.loading = false
        },
        clearSearch: (state) => {
            state.searchResults = []
            state.searchQuery = ''
            state.error = null
        },
    },
})

export const {
    setSearchQuery,
    setSearchResults,
    setLoading,
    setError,
    clearSearch,
} = genomesSlice.actions

export default genomesSlice.reducer
