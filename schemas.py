from pydantic import BaseModel
from datetime import date, time, datetime

class UserBase(BaseModel):
    email: str
    name: str
    date_of_birth: date
    gender: str

class UserCreate(UserBase):
    password: str

class PlaylistBase(BaseModel):
    playlist_name: str

class PlaylistCreate(PlaylistBase):
    user_email: str

class TrackBase(BaseModel):
    title: str
    duration: time
    artist: str
    album: str
    genre: str

class TrackCreate(TrackBase):
    pass
