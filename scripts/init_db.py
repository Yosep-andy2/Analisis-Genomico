#!/usr/bin/env python3
"""Initialize database with tables."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import engine
from app.db.base import Base

# Import all models
from app.models.genome import Genome
from app.models.analysis import Analysis
from app.models.result import Result
from app.models.validation import Validation


def init_db():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


if __name__ == "__main__":
    init_db()
