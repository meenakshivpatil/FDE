# Service layer for handling payment-related operations
from repository.payment import read_all_payments, read_payment_by_id, create_payment, update_payment, delete_payment
from models import Payment
def get_all_payments() -> list:
    return read_all_payments()

def get_payment_by_id(payment_id: str) -> Payment:
    return read_payment_by_id(payment_id)

def create_new_payment(payment: Payment) -> Payment:
    return create_payment(payment)

def update_existing_payment(payment_id: str, updated_payment: Payment) -> Payment:
    return update_payment(payment_id, updated_payment)

def delete_existing_payment(payment_id: str) -> Payment:
    return delete_payment(payment_id)

