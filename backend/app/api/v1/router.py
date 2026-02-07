"""API v1 router combining all endpoints."""

from fastapi import APIRouter
from app.api.v1.endpoints import genomes, analysis, results

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    genomes.router,
    prefix="/genomes",
    tags=["genomes"]
)

api_router.include_router(
    analysis.router,
    prefix="/analysis",
    tags=["analysis"]
)

api_router.include_router(
    results.router,
    prefix="/results",
    tags=["results"]
)
