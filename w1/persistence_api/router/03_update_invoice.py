#update invoice by ID
from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter()
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "data_store.json"

@router.put("/invoices/{invoice_id}")
def update_invoice(invoice_id: int, updated_invoice: dict):
    with open(DATA_FILE, "r") as file:
        invoices = json.load(file)
    for i, invoice in enumerate(invoices):
        if invoice["invoice_id"] == invoice_id:
            invoices[i].update(updated_invoice)
            with open(DATA_FILE, "w") as file:
                json.dump(invoices, file)
            return {"message": "Invoice updated successfully", "data": invoices[i]}
    return {"error": "Invoice not found"}