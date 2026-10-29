from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel

class Employee(BaseModel):
    id: int
    employee_id: str
    name: str
    department: str
    email: Optional[str] = None
    status: Literal["Active", "Inactive"] = "Active"

class review_period(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    status: Literal["Open", "Closed"] = "Open"


class performance_review_create(BaseModel):
    employee_id: int
    period_id: int
    quality_rating: int
    delivery_rating: int
    teamwork_rating: int
    comments: Optional[str] = None


class performance_review(BaseModel):
    id: int
    employee_id: int
    period_id: int
    quality_rating: int
    delivery_rating: int
    teamwork_rating: int
    average_rating: float
    created_at: datetime = datetime.now()
    comments: Optional[str] = None
    

   
   