from pydantic import BaseModel
class Invoice(BaseModel):
    invoice_id: int
    vendor: str
    amount: float
    status: str

class Employee(BaseModel):
    employee_id: int
    name: str
    department: str