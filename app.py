from fastapi import FastAPI
from pydantic import BaseModel
from textblob import TextBlob

app = FastAPI()

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