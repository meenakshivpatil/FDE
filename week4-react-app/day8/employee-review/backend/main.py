from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from models import *
import service
from typing import List, Optional
from typing_extensions import Literal
from database import get_db_connection


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
def health():
    cur = get_db_connection()
    cur.execute("SELECT 1")
    result = cur.fetchone()
    return {"db": "ok" if result else "error"}

@app.get("/employees", response_model=List[Employee])
def get_employees():
    try:
        return service.get_employees()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/review-periods", response_model=List[review_period])
def get_review_periods():
    try:
        return service.get_review_periods()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reviews", response_model=List[performance_review])
def get_reviews():
    try:
        return service.get_performance_reviews()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reviews/{review_id}", response_model=performance_review)
def get_review(review_id: int):
    try:
        review = service.get_performance_review(review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return review
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reviews", response_model=performance_review)
def create_review(review: performance_review_create):
    try:
        return service.create_performance_review(review)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))