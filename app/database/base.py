from sqlalchemy import UUID, Column, DateTime
from sqlalchemy.orm import DeclarativeBase
import uuid
from app.core.datetime_utils import utc_now_naive

class Base(DeclarativeBase):
    """Base class for all models."""
    id = Column(UUID, primary_key=True, default=uuid.uuid4, nullable=False)
    created_at = Column(DateTime, default=utc_now_naive, nullable=False)
    modified_at = Column(DateTime, default=utc_now_naive, onupdate=utc_now_naive, nullable=False)