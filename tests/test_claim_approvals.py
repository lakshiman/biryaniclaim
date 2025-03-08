import unittest
import os
import csv
from biryaniclaim.src.claim_approval import approve_claim, reject_claim, DATA_FILE

class TestClaimApprovals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary claims file for testing
        cls.test_data_file = DATA_FILE
        cls.test_claims = [
            {"claim_id": "1", "policy_number": "P123", "claim_amount": "1000.0", "date_of_incident": "2025-01-01", "status": "Submitted", "payout_amount": "0.0", "rejection_reason": ""},
            {"claim_id": "2", "policy_number": "P124", "claim_amount": "2000.0", "date_of_incident": "2025-02-01", "status": "Submitted", "payout_amount": "0.0", "rejection_reason": ""}
        ]
        os.makedirs(os.path.dirname(cls.test_data_file), exist_ok=True)
        with open(cls.test_data_file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=cls.test_claims[0].keys())
            writer.writeheader()
            writer.writerows(cls.test_claims)

    @classmethod
    def tearDownClass(cls):
        # Remove the temporary claims file after testing
        if os.path.exists(cls.test_data_file):
            os.remove(cls.test_data_file)

    def test_approve_claim(self):
        approve_claim(1, 1500.0)
        with open(self.test_data_file, "r") as file:
            reader = csv.DictReader(file)
            claims = list(reader)
        self.assertEqual(claims[0]["status"], "Approved")
        self.assertEqual(float(claims[0]["payout_amount"]), 1500.0)
        self.assertEqual(claims[0]["rejection_reason"], "")

    def test_reject_claim(self):
        reject_claim(2, "Insufficient documentation")
        with open(self.test_data_file, "r") as file:
            reader = csv.DictReader(file)
            claims = list(reader)
        self.assertEqual(claims[1]["status"], "Rejected")
        self.assertEqual(float(claims[1]["payout_amount"]), 0.0)
        self.assertEqual(claims[1]["rejection_reason"], "Insufficient documentation")

    def test_claim_not_found(self):
        with self.assertLogs(level='INFO') as log:
            approve_claim(3, 1000.0)
            self.assertIn("Claim ID 3 not found.", log.output)

if __name__ == "__main__":
    unittest.main()