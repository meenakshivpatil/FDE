# Route to delete an invoice by ID
from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter()
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "data_store.json"

@router.delete("/invoices/{invoice_id}")
def delete_invoice(invoice_id: int):
    with open(DATA_FILE, "r") as file:
        invoices = json.load(file)
    for i, invoice in enumerate(invoices):
        if invoice["invoice_id"] == invoice_id:
            deleted_invoice = invoices.pop(i)
            with open(DATA_FILE, "w") as file:
                json.dump(invoices, file)
            return {"message": "Invoice deleted successfully", "data": deleted_invoice}
    return {"error": "Invoice not found"}