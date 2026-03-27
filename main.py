import os
import sys
import json

# Graceful import with fallback if negotiate.py is missing
try:
    from negotiate import generate_email
except ImportError:
    def generate_email(service, price):
        return (
            f"Subject: Subscription Cancellation Request – {service}\n\n"
            f"Hi {service} Support,\n\n"
            f"I'm currently paying {price}/month and am considering cancelling "
            f"my subscription. I wanted to reach out first to see if there are "
            f"any retention offers or discounts available before I make a final decision.\n\n"
            f"Please let me know what options are available.\n\n"
            f"Thank you,\n[Your Name]"
        )

from scanner import scan_files

DB = "detected_subs.json"

def load_subs():
    try:
        with open(DB, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def parse_price(price_str):
    """Extract numeric value from price string like '$19.99' or '19.99'"""
    if not price_str:
        return 0.0
    cleaned = price_str.replace('$', '').replace(',', '').replace(' ', '')
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def view_stats():
    subs = load_subs()
    if not subs:
        print("\n  No subscriptions found. Run a scan first!")
        return

    print(f"\n  Found {len(subs)} subscription(s):\n")

    total = 0.0
    for sub in subs:
        svc = sub.get("service", "Unknown")
        price_str = sub.get("price", "0")
        price = parse_price(price_str)
        total += price
        print(f"  • {svc}: {price_str or 'N/A'}")  # Fix: was \x95 (Windows-1252 bullet)

    monthly = total
    annual = monthly * 12

    print(f"\n{'='*30}")
    print(f"  MONTHLY BURN: ${monthly:.2f}")
    print(f"  ANNUAL BURN:  ${annual:.2f}")

    if monthly > 50:
        print(f"\n  Ouch! Time to negotiate!")
    elif monthly > 0:
        print(f"\n  Not bad, but every dollar counts!")
    print(f"{'='*30}\n")

def main_menu():
    print("\n---  SubVibe: Your Subscription Manager ---")
    print("1. Scan for Subscriptions (Select Folder)")
    print("2. Generate Negotiation Email")
    print("3. View Stats")
    print("4. Exit")

    choice = input("\nWhat would you like to do? ").strip()

    if choice == '1':
        path = input("Enter the path to your receipts folder: ").strip()
        if os.path.exists(path):
            scan_files(path)
            print("\n  Scan complete! Check detected_subs.json.")
        else:
            print("  Path not found. Please check the folder path and try again.")

    elif choice == '2':
        service = input("Enter the service name (e.g., Adobe, Netflix): ").strip()
        price = input("Enter current price: ").strip()
        if not service:
            print("  Service name cannot be empty.")
            return
        email_body = generate_email(service, price)
        print("\n---  Drafted Email ---\n")
        print(email_body)
        print("\n--- End of Draft ---")

    elif choice == '3':
        view_stats()

    elif choice == '4':
        print("Stay vibey. Goodbye!")
        sys.exit(0)  # Fix: exit() is a REPL helper; sys.exit() is correct for scripts

    else:
        print("  Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    while True:
        main_menu()
