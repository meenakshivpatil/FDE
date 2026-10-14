from typing import Optional

from pydantic import BaseModel

class Invoice(BaseModel):
    invoice_id: str
    vendor: str
    amount: Optional[float] = None
    status: str ="UNKNOWN"
    date: str = "UNKNOWN"
    total_payment: float = 0.0


class Payment(BaseModel):
    invoice_id: str
    paid: float

