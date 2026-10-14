from fastapi import FastAPI
from data_store import invoices
from models import Invoice
import json
from pathlib import Path
from fastapi import APIRouter

router = APIRouter()
DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "data_store.json"

@router.post("/invoices")
def create_invoice(invoice: Invoice):
    new_invoice = invoice.model_dump()  # Convert the Pydantic model to a dictionary
    
    with open(DATA_FILE, "r") as file:
        invoices = json.load(file)
    invoices.append(new_invoice)

    # Write the updated invoices list back to the JSON file
    with open(DATA_FILE, "w") as file:
     
     # Use json.dump(). Dump the updated invoices list into the file
          json.dump(invoices, file)
    return {"message": "Invoice created successfully", "data": new_invoice}