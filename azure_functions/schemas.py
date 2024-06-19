from pydantic import BaseModel, condecimal
from typing import Optional


class PlayerSeasonStats(BaseModel):
    player_id: int
    player_name: str
    season: str
    age: Optional[int] = 0
    position: Optional[str] = ''
    height: Optional[str] = ''
    weight: Optional[str] = ''
    rating: Optional[condecimal(gt=0, le=10)] = 0.0
    games_appearences: Optional[int] = 0
    games_lineups: Optional[int] = 0
    minutes_played: Optional[int] = 0
    goals_total: Optional[int] = 0
    passes_total: Optional[int] = 0
    passes_accuracy: Optional[int] = 0
    dribbles_attempts: Optional[int] = 0
    dribbles_success: Optional[int] = 0
    tackles_total: Optional[int] = 0
    fouls_committed: Optional[int] = 0

    class Config:
        from_attributes = True
