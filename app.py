from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from textblob import TextBlob

app = FastAPI()

# Tambahkan Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Ganti dengan domain frontend Anda
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua metode (GET, POST, dll.)
    allow_headers=["*"],  # Mengizinkan semua header
)

class QueryRequest(BaseModel):
    query: str

@app.post("/analyze-sentiment/")
def analyze_sentiment(request: QueryRequest):
    query = request.query
    sentiment = TextBlob(query).sentiment.polarity
    mood = "neutral"
    if sentiment < -0.2:
        mood = "sad"
    elif sentiment > 0.2:
        mood = "happy"
    return {"query": query, "sentiment": sentiment, "mood": mood}
