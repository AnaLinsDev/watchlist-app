from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class WatchlistItem(Base):
    __tablename__ = "watchlist_items"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    type = Column(String)

    watchlist_id = Column(Integer, ForeignKey("watchlists.id"))

    watchlist = relationship("Watchlist", back_populates="items")