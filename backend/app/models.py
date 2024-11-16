from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    rating: int 
    games_played: int
    wins: int
    losses: int
