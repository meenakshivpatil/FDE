from fastapi import FastAPI, HTTPException

from router.invoice import router as invoice
from router.payment import router as payment
from router.reconciliation import router as reconciliation

app = FastAPI()

app.include_router(invoice)
app.include_router(payment)
app.include_router(reconciliation)

