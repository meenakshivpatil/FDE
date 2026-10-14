#1. Create a Python program named:
from ast import For
import csv


#2. read csv file containing invoice data.
with open('../data/homework_invoices.csv', newline='') as csvfile:
    invoice_reader = csv.reader(csvfile)
    for row in invoice_reader:
        print(row) 


#3. For each invoice, read and check the following details:Vendor, Amount, and Status.
with open('../data/homework_invoices.csv', newline='') as csvfile:
    invoice_reader = csv.DictReader(csvfile)
    t_invoice_reader = type(invoice_reader)
    print(f"Type of invoice_reader: {t_invoice_reader}")
    for row in invoice_reader:
        invoice_id = row.get("invoice_id")
        vendor = row.get("vendor")
        amount = row.get("amount")
        status = row.get("status")
        print(f"Invoice ID: {invoice_id}, Vendor: {vendor}, Amount: {amount}, Status: {status}")
 
#4. Check the invoice amount:
#   - Identify invoices where the amount is greater than 100,000.
#   - Identify missing or invalid amount values.
with open('../data/homework_invoices.csv', newline='') as csvfile:
    invoice_reader = csv.DictReader(csvfile)
    for row in invoice_reader:
        invoice_id = row.get("invoice_id")
        vendor = row.get("vendor")
        amount = row.get("amount")
        status = row.get("status")
        try:
            amount_value = float(amount)
            if amount_value > 100000:
                print(f"High amount invoice - Invoice ID: {invoice_id}, Vendor: {vendor}, Amount: {amount}, Status: {status}")
        except (ValueError, TypeError):
            print(f"Invalid or missing amount - Invoice ID: {invoice_id}, Vendor: {vendor}, Amount: {amount}, Status: {status}")

# 6. Print a simple summary at the end:
#    - Total invoices read
#    - Number of invoices greater than 100,000
#    - Number of invoices with missing/invalid amount

total_invoices = 0
high_amount_invoices = 0
invalid_amount_invoices = 0

with open('../data/homework_invoices.csv', newline='') as csvfile:
    invoice_reader = csv.DictReader(csvfile)
    for row in invoice_reader:
        total_invoices += 1
        invoice_id = row.get("invoice_id")
        vendor = row.get("vendor")
        amount = row.get("amount")
        status = row.get("status")
        try:
            amount_value = float(amount)
            if amount_value > 100000:
                high_amount_invoices += 1
        except (ValueError, TypeError):
            invalid_amount_invoices += 1

print(f"Total invoices read: {total_invoices}")
print(f"Number of invoices greater than 100,000: {high_amount_invoices}")
print(f"Number of invoices with missing/invalid amount: {invalid_amount_invoices}")

#7 Write matching records into another CSV 
#    - Only invoices with amount greater than 100,000 will be written to the new CSV file.


with open('../data/homework_invoices.csv', newline='') as csvfile, open('../data/high_amount_invoices.csv', 'w', newline='') as outfile:
    invoice_reader = csv.DictReader(csvfile)
    fieldnames = invoice_reader.fieldnames
    print(f"Fieldnames: {fieldnames}")
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in invoice_reader:
        try:
            amount_value = float(row.get("amount"))
            if amount_value > 100000:
                writer.writerow(row)
        except (ValueError, TypeError):
            continue

#8 group by vendor
from collections import defaultdict

vendor_invoices = defaultdict(list)

with open('../data/homework_invoices.csv', newline='') as csvfile:
    invoice_reader = csv.DictReader(csvfile)
    for row in invoice_reader:
        try:
            amount_value = float(row.get("amount"))
            if amount_value > 100000:
                vendor_invoices[row.get("vendor")].append(row)
        except (ValueError, TypeError):
            continue

with open('../data/high_amount_invoices_by_vendor.csv', 'w', newline='') as outfile:
    fieldnames = ["invoice_id", "vendor", "amount", "status"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for vendor, invoices in vendor_invoices.items():
        for invoice in invoices:
            writer.writerow(invoice)

