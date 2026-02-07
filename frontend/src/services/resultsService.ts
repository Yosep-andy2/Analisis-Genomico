import apiClient from './api'

export interface CompleteAnalysisResult {
    analysis_id: number
    genome_accession: string
    organism: string
    status: string
    codon_analysis?: any
    gene_stats?: any
    genome_stats?: any
    validation?: any
    charts?: Record<string, string>
}

export interface ResultResponse {
    id: number
    analysis_id: number
    result_type: string
    data: any
    created_at: string
}

export const resultsService = {
    /**
     * Get complete analysis results
     */
    getComplete: async (analysisId: number): Promise<CompleteAnalysisResult> => {
        const response = await apiClient.get(`/results/${analysisId}`)
        return response.data
    },

    /**
     * Get raw result records
     */
    getRaw: async (analysisId: number): Promise<ResultResponse[]> => {
        const response = await apiClient.get(`/results/${analysisId}/raw`)
        return response.data
    },
}
