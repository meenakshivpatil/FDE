from fastapi import FastAPI
import json
from pathlib import Path
from data_store import invoices
from fastapi import APIRouter

router = APIRouter()
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "data_store.json"
#1 Route to get all invoices
@router.get("/invoices")
def get_invoices():
    with open(DATA_FILE, "r") as file:
        invoices = json.load(file)
    return {"message": "List of invoices", "data": invoices}

#2 Route to get a specific invoice by ID
@router.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int):
    with open(DATA_FILE, "r") as file:
        invoices = json.load(file)
    for invoice in invoices:
        if invoice["invoice_id"] == invoice_id:
            return invoice
    return {"error": "Invoice not found"}