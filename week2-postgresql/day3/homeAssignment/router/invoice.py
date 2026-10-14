from fastapi import APIRouter
import json
from pathlib import Path
import services.invoice as invoice_service
from models import Invoice

router = APIRouter()

router = APIRouter()
DATA_FILE = Path(__file__).resolve().parents[2] / "dataHomeAssignment" / "invoices.json"

#1 Route to get all invoices
@router.get("/invoices")
def get_invoices():
    return invoice_service.read_all_invoices()


#2 Route to get a single invoice by its ID
@router.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: str):
    return invoice_service.read_invoice_by_id(invoice_id)

#3 Route to create a new invoice
@router.post("/invoices")
def create_invoice(invoice: Invoice):
    return invoice_service.create_invoice(invoice)

#4 Route to update an existing invoice by its ID
@router.put("/invoices/{invoice_id}")
def update_invoice(invoice_id: str, updated_invoice: Invoice):
    return invoice_service.update_invoice(invoice_id, updated_invoice)

#5 Route to delete an existing invoice by its ID
@router.delete("/invoices/{invoice_id}")
def delete_invoice(invoice_id: str):
    return invoice_service.delete_invoice(invoice_id)   

