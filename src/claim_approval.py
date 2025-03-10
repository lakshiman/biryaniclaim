import csv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get the absolute path to the data folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Path to the src folder
DATA_FILE = os.path.join(BASE_DIR, "..", "data", "claims.csv")

def approve_claim(claim_id, payout_amount):
    update_claim_status(claim_id, "Approved", payout_amount, "")

def reject_claim(claim_id, rejection_reason):
    update_claim_status(claim_id, "Rejected", 0.0, rejection_reason)

def update_claim_status(claim_id, status, payout_amount, rejection_reason):
    if not os.path.exists(DATA_FILE):
        logging.info("No claims file found.")
        return

    claims = []
    with open(DATA_FILE, "r") as file:
        reader = csv.DictReader(file)
        claims = list(reader)
        if not claims:
            logging.info("Claims file is empty.")
            return

    claim_found = False
    for claim in claims:
        if int(claim["claim_id"]) == claim_id:
            claim["status"] = status
            claim["payout_amount"] = payout_amount
            claim["rejection_reason"] = rejection_reason
            claim_found = True
            break

    if not claim_found:
        logging.info(f"Claim ID {claim_id} not found.")
        return

    with open(DATA_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=claims[0].keys())
        writer.writeheader()
        writer.writerows(claims)

    logging.info(f"Claim ID {claim_id} has been {status.lower()}.")

# Example usage:
# approve_claim(1, 1000.0)
# reject_claim(2, "Insufficient documentation")