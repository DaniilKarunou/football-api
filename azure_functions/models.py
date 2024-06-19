from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PlayerSeasonStats(Base):
    __tablename__ = 'player_season_stats'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, nullable=False)
    player_name = Column(String)
    season = Column(String)
    age = Column(Integer)
    height = Column(String)
    weight = Column(String)
    rating = Column(Float)
    games_appearences = Column(Integer)
    games_lineups = Column(Integer)
    minutes_played = Column(Integer)
    goals_total = Column(Integer)
    passes_total = Column(Integer)
    passes_accuracy = Column(Integer)
    dribbles_attempts = Column(Integer)
    dribbles_success = Column(Integer)
    tackles_total = Column(Integer)
    fouls_committed = Column(Integer)