import os
import csv
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.claim_submission import submit_claim, get_next_claim_id

def test_submit_claim():
    # Backup the existing claims file (if it exists)
    backup_file = None
    if os.path.exists("/claims.csv"):
        with open("data/claims.csv", "r") as file:
            backup_file = file.read()

    # Test submitting a new claim
    submit_claim("POL123", 1000.0, "2023-10-01")

    # Verify the new claim was appended with the correct ID
    with open("data/claims.csv", "r") as file:
        reader = csv.DictReader(file)
        claims = list(reader)
        assert len(claims) > 0  # Ensure at least one claim exists
        last_claim = claims[-1]  # Get the last claim in the file
        expected_id = str(len(claims))  # claim_id should match the row count
        assert last_claim["claim_id"] == expected_id
        assert last_claim["policy_number"] == "POL123"
        assert last_claim["claim_amount"] == "1000.0"
        assert last_claim["status"] == "Submitted"

    # Clean up: Restore the original claims file
    if backup_file:
        with open("data/claims.csv", "w") as file:
            file.write(backup_file)
    else:
        os.remove("data/claims.csv")  # Delete the file if it didn't exist before

