from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.mixins import TimestampMixin


class Watchlist(Base, TimestampMixin):
    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    items_count = Column(Integer, default=0, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    user = relationship("User", back_populates="watchlists")

    items = relationship(
        "WatchlistItem",
        back_populates="watchlist",
        cascade="all, delete-orphan",
        lazy="selectin"  # Avoid N+1 problem
    )

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_watchlist_name"),
    )
