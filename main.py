import os
import json
from scanner import scan_files
from negotiate import generate_email

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
    # Remove $ and spaces, handle commas
    cleaned = price_str.replace('$', '').replace(',', '').replace(' ', '')
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def view_stats():
    subs = load_subs()
    if not subs:
        print("\n No subscriptions found. Run a scan first!")
        return
    
    print(f"\n Found {len(subs)} subscription(s):\n")
    
    total = 0.0
    for sub in subs:
        svc = sub.get("service", "Unknown")
        price_str = sub.get("price", "0")
        price = parse_price(price_str)
        total += price
        print(f"  • {svc}: {price_str or 'N/A'}")
    
    monthly = total
    annual = monthly * 12
    
    print(f"\n{'='*30}")
    print(f" MONTHLY BURN: ${monthly:.2f}")
    print(f" ANNUAL BURN:  ${annual:.2f}")
    
    if monthly > 50:
        print(f"\n Ouch! Time to negotiate!")
    elif monthly > 0:
        print(f"\n Not bad, but every dollar counts!")
    print(f"{'='*30}\n")

def main_menu():
    print("\n---  SubVibe: Your Android Subscription Manager ---")
    print("1. Scan for Subscriptions (Select Folder)")
    print("2. Generate Negotiation Email")
    print("3. View Stats")
    print("4. Exit")
    
    choice = input("\nWhat would you like to do? ")

    if choice == '1':
        path = input("Enter the path to your receipts folder (e.g., /sdcard/Download): ")
        if os.path.exists(path):
            scan_files(path)
            print("\n Scan complete! Check detected_subs.json.")
        else:
            print(" Path not found.")
            
    elif choice == '2':
        service = input("Enter the service name (e.g., Adobe, Netflix): ")
        price = input("Enter current price: ")
        email_body = generate_email(service, price)
        print("\n---  Drafted Email ---\n")
        print(email_body)
        print("\n--- End of Draft ---")

    elif choice == '3':
        view_stats()

    elif choice == '4':
        print("Stay vibey. Goodbye!")
        exit()
    else:
        print(" Invalid choice. Try 1-4.")

if __name__ == "__main__":
    while True:
        main_menu()
        