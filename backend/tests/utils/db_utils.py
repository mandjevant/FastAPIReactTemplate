"""Module to help with SQLite compatibility for testing."""

from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import JSONB


# Patch SQLAlchemy's JSONB type for SQLite compatibility
# This ensures SQLite can handle JSONB columns by treating them as regular JSON
class JSONBSQLite(JSON):
    """A SQLite-compatible version of JSONB."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# Save the original JSONB for reference
original_jsonb = JSONB
