import services.invoice as invoices_service
import services.payment as payments_service



def normalize_invoices(invoices):
    for i, invoice in enumerate(invoices):
        if invoice.amount is None:
            print(f"Invoice at index {i} has no amount")
            continue
        invoice.vendor = invoice.vendor.strip().title()
        invoice.status = invoice.status.upper()
    return invoices


def remove_exact_duplicates(invoices):
    exact_dupes = {}
    sorted_indexes = []

    for i, invoice in enumerate(invoices):
        key = tuple(invoice.model_dump().values())
        if key not in exact_dupes:
            exact_dupes[key] = []
        exact_dupes[key].append(i)

    # Return the duplicate groups and the indexes to remove later in the calling function.
    for key, indexes in exact_dupes.items():
        ordered_indexes = sorted(indexes, reverse=True)
        if len(ordered_indexes) > 1:
            sorted_indexes.extend(ordered_indexes[1:])

    return exact_dupes, sorted(sorted_indexes, reverse=True)

def find_suspected_duplicates(invoices):
    suspected_dupes = []
    for i, invoice1 in enumerate(invoices):
        for j in range(i + 1, len(invoices)):
            invoice2 = invoices[j]
            if (
                invoice1.vendor == invoice2.vendor and
                invoice1.amount == invoice2.amount and
                invoice1.date == invoice2.date and
                invoice1.invoice_id != invoice2.invoice_id
            ):
                suspected_dupes.append((invoice2.invoice_id, invoice1.invoice_id))
    return suspected_dupes


def perform_credit_note_reconciliation(invoices):
    for i, invoice in enumerate(invoices):
        if invoice.amount is not None and invoice.amount < 0:
            partner_found = False
            for j, potential_partner in enumerate(invoices):
                if (
                    i != j
                    and potential_partner.amount is not None
                    and invoice.vendor == potential_partner.vendor
                    and invoice.amount == -potential_partner.amount
                ):
                    invoice.status = "CANCELLED"
                    potential_partner.status = "CANCELLED"
                    print(f"Credit note matched: {i} <-> {j}")
                    partner_found = True
                    break
            if not partner_found:
                print(f"Credit note with no partner: {i}")
    return invoices


def reconcile_payments(invoices, payments):
    for invoice in invoices:
        if invoice.amount is None or invoice.status == "CANCELLED":
            continue
        total_payment = sum(
            payment["paid"] for payment in payments if payment["invoice_id"] == invoice.invoice_id
        )
        invoice.total_payment = total_payment
        if total_payment == invoice.amount:
            invoice.status = "PAID"
        elif total_payment > 0:
            invoice.status = "PARTIALLY_PAID"
        else:
            invoice.status = "UNPAID"
    return invoices



def perform_reconciliation():
    #Normalize invoices. Clean the vendor (strip, title-case) and the status (upper-case). Do it in place using the index. Report any row where amount is None, with its index, and exclude it from the later totals.

    # Read all invoices and payments
    invoices= invoices_service.read_all_invoices()
    payments= payments_service.get_all_payments()

    # 1 Normalize invoices
    invoices = normalize_invoices(invoices)
    print("Invoices after normalization:", invoices)

    # 2 Exact duplicates.
    exact_dupes, indexes_to_remove = remove_exact_duplicates(invoices)
    print("Indexes to remove for exact duplicates:", indexes_to_remove)
    print("Exact duplicate groups before removal:", exact_dupes)

    for idx in indexes_to_remove:
        del invoices[idx]
    print("Invoices after removing exact duplicates:", invoices)


    # 3 Suspected duplicates.
    # Don't remove rows while looping forward, because that skips items. Not implemented anything for this
    #3 Suspected duplicates. Find rows that match on vendor, amount and date but have different IDs. 
    #Print them as pairs, (INV-107 ~ INV-101), and don't remove them.

    suspected_dupes = find_suspected_duplicates(invoices)
    print("Suspected duplicate pairs:", suspected_dupes)


    # 4. Credit notes. Match each negative invoice to its positive partner. 
    # Mark both as "CANCELLED" and exclude them from totals. 
    # Print the index pair, for example 3 <-> 6. Handle a credit note with no partner.

    invoices =  perform_credit_note_reconciliation(invoices)
    print("Invoices after credit note reconciliation:", invoices)


    # 5 5) Reconcile payments. 
    #Join payments to invoices by invoice_id. 
    #Sum the payments for each invoice. Then print:

    reconciled_invoices = reconcile_payments(invoices, payments)
    print("Invoices after payment reconciliation:", reconciled_invoices)

    return invoices
    