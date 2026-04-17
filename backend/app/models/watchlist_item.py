from sqlalchemy import Column, Integer, String, ForeignKey, Text, UniqueConstraint, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.mixins import TimestampMixin
import enum

class MediaType(enum.Enum):
    movie = "movie"
    tv = "tv"

class WatchlistItem(Base, TimestampMixin):
    __tablename__ = "watchlist_items"

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    type = Column(Enum(MediaType, name="media_type"), nullable=False)  # movie / tv

    tmdb_id = Column(Integer, nullable=False)

    notes = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)  # 0–5

    watchlist_id = Column(Integer, ForeignKey("watchlists.id"), nullable=False)

    watchlist = relationship("Watchlist", back_populates="items")

    __table_args__ = (
        UniqueConstraint("watchlist_id", "tmdb_id", name="uq_watchlist_tmdb"),
    )