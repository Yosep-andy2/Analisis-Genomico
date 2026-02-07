import { configureStore } from '@reduxjs/toolkit'
import genomesReducer from './slices/genomesSlice'
import analysisReducer from './slices/analysisSlice'

export const store = configureStore({
    reducer: {
        genomes: genomesReducer,
        analysis: analysisReducer,
    },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
