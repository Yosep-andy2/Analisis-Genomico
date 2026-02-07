import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface AnalysisStatus {
    analysis_id: number
    task_id: string
    status: string
    progress: number
    message?: string
    started_at?: string
    completed_at?: string
}

interface AnalysisState {
    currentAnalysis: AnalysisStatus | null
    analyses: AnalysisStatus[]
    loading: boolean
    error: string | null
}

const initialState: AnalysisState = {
    currentAnalysis: null,
    analyses: [],
    loading: false,
    error: null,
}

const analysisSlice = createSlice({
    name: 'analysis',
    initialState,
    reducers: {
        setCurrentAnalysis: (state, action: PayloadAction<AnalysisStatus>) => {
            state.currentAnalysis = action.payload
            state.loading = false
            state.error = null
        },
        updateAnalysisStatus: (state, action: PayloadAction<AnalysisStatus>) => {
            state.currentAnalysis = action.payload

            // Update in analyses list if exists
            const index = state.analyses.findIndex(a => a.analysis_id === action.payload.analysis_id)
            if (index !== -1) {
                state.analyses[index] = action.payload
            }
        },
        setAnalyses: (state, action: PayloadAction<AnalysisStatus[]>) => {
            state.analyses = action.payload
            state.loading = false
        },
        setLoading: (state, action: PayloadAction<boolean>) => {
            state.loading = action.payload
        },
        setError: (state, action: PayloadAction<string>) => {
            state.error = action.payload
            state.loading = false
        },
        clearCurrentAnalysis: (state) => {
            state.currentAnalysis = null
        },
    },
})

export const {
    setCurrentAnalysis,
    updateAnalysisStatus,
    setAnalyses,
    setLoading,
    setError,
    clearCurrentAnalysis,
} = analysisSlice.actions

export default analysisSlice.reducer
