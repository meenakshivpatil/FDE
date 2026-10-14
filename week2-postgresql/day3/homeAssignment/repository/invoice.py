import json
DATA_INVOICE_FILE = "dataHomeAssignment/invoices.json"

# Read all invoices from the JSON file
def read_all_invoices() -> list:
    with open(DATA_INVOICE_FILE, 'r') as file:
        data = json.load(file)
        print(data)
        return data

# Create a new invoice and save it to the JSON file
def create_invoice(invoice: dict) -> dict:
    invoices = read_all_invoices()
    invoices.append(invoice)
    with open(DATA_INVOICE_FILE, 'w') as file:
        json.dump(invoices, file, indent=4)
    return invoice

# Update an existing invoice by its ID
def update_invoice(invoice_id: str, updated_invoice: dict) -> dict | None:
    invoices = read_all_invoices()
    for idx, inv in enumerate(invoices):
        if inv["invoice_id"] == invoice_id:
            invoices[idx] = updated_invoice
            with open(DATA_INVOICE_FILE, 'w') as file:
                json.dump(invoices, file, indent=4)
            return updated_invoice
    return None

# Delete an existing invoice by its ID
def delete_invoice(invoice_id: str) -> dict | None:
    invoices = read_all_invoices()
    for idx, inv in enumerate(invoices):
        if inv["invoice_id"] == invoice_id:
            deleted_invoice = invoices.pop(idx)
            with open(DATA_INVOICE_FILE, 'w') as file:
                json.dump(invoices, file, indent=4)
            return deleted_invoice
    return None


