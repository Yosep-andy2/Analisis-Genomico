import apiClient from './api'

export interface GenomeSearchResult {
    accession: string
    title: string
    organism: string
    length: number
    update_date: string
    gi?: string
}

export interface GenomeDetail extends GenomeSearchResult {
    create_date: string
    taxonomy: string
}

export const genomesService = {
    /**
     * Search for genomes in NCBI
     */
    search: async (query: string, limit: number = 20): Promise<GenomeSearchResult[]> => {
        const response = await apiClient.get('/genomes/search', {
            params: { query, limit },
        })
        return response.data
    },

    /**
     * Get genome details by accession
     */
    getDetails: async (accession: string): Promise<GenomeDetail> => {
        const response = await apiClient.get(`/genomes/${accession}`)
        return response.data
    },
}
