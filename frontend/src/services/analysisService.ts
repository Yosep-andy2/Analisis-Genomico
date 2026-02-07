import apiClient from './api'

export interface AnalysisRequest {
    accession: string
}

export interface AnalysisStatus {
    analysis_id: number
    task_id: string
    status: string
    progress: number
    message?: string
    started_at?: string
    completed_at?: string
}

export interface AnalysisResponse {
    id: number
    genome_id: number
    task_id?: string
    status: string
    progress: number
    started_at: string
    completed_at?: string
    error_message?: string
}

export const analysisService = {
    /**
     * Start a new genome analysis
     */
    start: async (accession: string): Promise<AnalysisStatus> => {
        const response = await apiClient.post('/analysis/start', { accession })
        return response.data
    },

    /**
     * Get analysis status by ID
     */
    getStatus: async (analysisId: number): Promise<AnalysisStatus> => {
        const response = await apiClient.get(`/analysis/${analysisId}`)
        return response.data
    },

    /**
     * List all analyses
     */
    list: async (skip: number = 0, limit: number = 100): Promise<AnalysisResponse[]> => {
        const response = await apiClient.get('/analysis/', {
            params: { skip, limit },
        })
        return response.data
    },
}
