from fastapi import APIRouter
import models
from services.payment import get_all_payments, get_payment_by_id, create_new_payment, update_existing_payment, delete_existing_payment
router = APIRouter()

@router.get("/payments")
def read_all_payments():
    return get_all_payments()

@router.get("/payments/{payment_id}")
def read_payment(payment_id: str):
    return get_payment_by_id(payment_id)

@router.post("/payments")
def create_payment(payment: models.Payment):
    return create_new_payment(payment)

@router.put("/payments/{payment_id}")
def update_payment(payment_id: str, updated_payment: models.Payment):
    return update_existing_payment(payment_id, updated_payment)

@router.delete("/payments/{payment_id}")
def delete_payment(payment_id: str):
    return delete_existing_payment(payment_id)