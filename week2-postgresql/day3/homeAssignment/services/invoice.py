import repository.invoice as repoinv

from models import Invoice
import json


# Read all invoices from the JSON file
def read_all_invoices() -> list[Invoice]:
    invoices_data = repoinv.read_all_invoices()
    return [Invoice(**inv) for inv in invoices_data]

# Read a single invoice by its ID
def read_invoice_by_id(invoice_id: str) -> Invoice:
    invoices_data = repoinv.read_all_invoices()
    for inv in invoices_data:
        if inv["invoice_id"] == invoice_id:
            return Invoice(**inv)
    return None

# Create a new invoice, using function in the repository, dont open file here
def create_invoice(invoice: Invoice) -> Invoice:
    created_invoice = repoinv.create_invoice(invoice.model_dump())
    return Invoice(**created_invoice)

# Update an existing invoice by its ID, using function in the repository, dont open file here
def update_invoice(invoice_id: str, updated_invoice: Invoice) -> Invoice:
    invoices_data = repoinv.read_all_invoices()
    for idx, inv in enumerate(invoices_data):
        if inv["invoice_id"] == invoice_id:
            updated_invoice_data = updated_invoice.model_dump()
            updated_invoice_result = repoinv.update_invoice(invoice_id, updated_invoice_data)
            if updated_invoice_result:
                return Invoice(**updated_invoice_result)
    return None

# Delete an existing invoice by its ID, using function in the repository, dont open file here
def delete_invoice(invoice_id: str) -> bool:
    invoices_data = repoinv.read_all_invoices()
    for idx, inv in enumerate(invoices_data):
        if inv["invoice_id"] == invoice_id:
            result = repoinv.delete_invoice(invoice_id)
            return result is not None
    return False

