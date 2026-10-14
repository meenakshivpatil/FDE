from fastapi import APIRouter
import services.reconciliation as reconciliation_service
router = APIRouter()

@router.post("/reconciliations")
def reconcile_invoices():
    #call the reconciliation service or function here
    invoices = reconciliation_service.perform_reconciliation()  # Example function call to perform the reconciliation process
    return {"detail": "Reconciliation process executed successfully", "invoices": invoices}