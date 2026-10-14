# Repository for handling payment-related operations
import json
from pathlib import Path
from fastapi import HTTPException
from models import Payment


DATA_PAYMENT_FILE = Path(__file__).resolve().parents[2] / "homeAssignment" / "dataHomeAssignment" / "payments.json"

def read_all_payments() -> list:
    with open(DATA_PAYMENT_FILE, 'r') as file:
        return json.load(file)

def read_payment_by_id(payment_id: str) -> Payment:
    with open(DATA_PAYMENT_FILE, 'r') as file:
        payments = json.load(file)
        for payment in payments:
            if payment["invoice_id"] == payment_id:
                return Payment(**payment)
    raise HTTPException(status_code=404, detail="Payment not found")

def create_payment(payment: Payment) -> Payment:
    with open(DATA_PAYMENT_FILE, 'r') as file:
        payments = json.load(file)
    payments.append(payment.model_dump())
    with open(DATA_PAYMENT_FILE, 'w') as file:
        json.dump(payments, file, indent=4)
    return payment

def update_payment(payment_id: str, updated_payment: Payment) -> Payment:
    with open(DATA_PAYMENT_FILE, 'r') as file:
        payments = json.load(file)
    for i, payment in enumerate(payments):
        if payment["invoice_id"] == payment_id:
            payments[i] = updated_payment.model_dump()
            with open(DATA_PAYMENT_FILE, 'w') as file:
                json.dump(payments, file, indent=4)
            return updated_payment
    raise HTTPException(status_code=404, detail="Payment not found")


def delete_payment(payment_id: str) -> Payment:
    with open(DATA_PAYMENT_FILE, 'r') as file:
        payments = json.load(file)
    for i, payment in enumerate(payments):
        if payment["invoice_id"] == payment_id:
            del payments[i]
            with open(DATA_PAYMENT_FILE, 'w') as file:
                json.dump(payments, file, indent=4)
            return Payment(**payment)
    raise HTTPException(status_code=404, detail="Payment not found")

