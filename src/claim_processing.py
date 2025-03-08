import csv
import os

class ClaimProcessing:
    def __init__(self, data_file):
        self.data_file = data_file

    def process_claims(self):
        if not os.path.exists(self.data_file):
            print("No claims to process.")
            return

        claims = self.read_claims()
        processed_claims = []

        for claim in claims:
            if self.is_valid_claim(claim):
                claim["status"] = "Approved"
                claim["payout_amount"] = self.calculate_payout(claim)
            else:
                claim["status"] = "Rejected"
                claim["rejection_reason"] = "Invalid claim based on policy terms"
            processed_claims.append(claim)

        self.write_claims(processed_claims)

    def read_claims(self):
        with open(self.data_file, "r") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def write_claims(self, claims):
        with open(self.data_file, "w", newline="") as file:
            fieldnames = claims[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(claims)

    def is_valid_claim(self, claim):
        # Implement your policy terms validation logic here
        # For example, check if the claim amount is within a certain range
        return float(claim["claim_amount"]) > 0

    def calculate_payout(self, claim):
        # Implement your payout calculation logic here
        # For example, return a percentage of the claim amount
        return float(claim["claim_amount"]) * 0.8

# Example usage
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE = os.path.join(BASE_DIR, "..", "data", "claims.csv")
    processor = ClaimProcessing(DATA_FILE)
    processor.process_claims()