from fastapi import FastAPI
import importlib

create_invoice = importlib.import_module("router.03_create_invoice").router
get_invoices = importlib.import_module("router.03_get_invoice").router
delete_invoice = importlib.import_module("router.03_delete_invoice").router
update_invoice = importlib.import_module("router.03_update_invoice").router


app = FastAPI()
app.include_router(create_invoice)
app.include_router(get_invoices)
app.include_router(delete_invoice)
app.include_router(update_invoice)