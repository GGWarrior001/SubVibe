import json
import sys
from datetime import datetime

DB = "detected_subs.json"

def load_services():
    try:
        data = json.load(open(DB))
        # Deduplicate by service name, keep latest price
        seen = {}
        for entry in data:
            svc = entry.get("service") or "Unknown Service"
            seen[svc] = entry  # Overwrite to keep most recent
        return list(seen.items())
    except FileNotFoundError:
        print("No detected_subs.json found. Run scanner first.")
        sys.exit(1)

def generate_email(service, entry):
    price = entry.get("price") or "the current rate"
    svc_name = service if service != "Unknown Service" else "your service"
    
    template = f"""Subject: Request for Loyalty/Student Discount - {svc_name}

Dear {svc_name} Support Team,

I hope this message finds you well. I am writing regarding my subscription ({price}/month) and my intention to keep my account active.

However, due to current budget constraints [optional: as a student/recent graduate], I am exploring options to reduce my monthly expenses. I have greatly valued the service provided over the time I've been a subscriber.

Would you be able to offer a loyalty discount or student rate to help me continue my subscription? Many services offer retention rates of 20-50% off, which would make a significant difference for me.

I would appreciate any consideration you can provide. If a discount is not available at this time, I may need to proceed with cancellation.

Thank you for your understanding.

Best regards,
[Your Name]
"""
    return template

def main():
    services = load_services()
    
    if not services:
        print("No subscriptions found in database.")
        return
    
    print("\n💰 Detected Subscriptions:")
    for i, (name, entry) in enumerate(services, 1):
        price = entry.get("price") or "??"
        print(f"{i}. {name} ({price})")
    
    try:
        choice = int(input("\nPick number to negotiate: ").strip()) - 1
        if 0 <= choice < len(services):
            name, entry = services[choice]
            print("\n" + "="*50)
            print(generate_email(name, entry))
            print("="*50)
            print("\n📋 Copy the email above (long-press in Termux)")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()
