import os
from scanner import scan_receipts  # Importing your Kimi logic
# Assuming your negotiator logic is inside a function in negotiate.py
from negotiate import generate_email 

def main_menu():
    print("--- 📱 SubVibe: Your Android Subscription Manager ---")
    print("1. Scan for Subscriptions (Select Folder)")
    print("2. Generate Negotiation Email")
    print("3. Exit")
    
    choice = input("\nWhat would you like to do? ")

    if choice == '1':
        path = input("Enter the path to your receipts folder (e.g., /sdcard/Download): ")
        if os.path.exists(path):
            scan_receipts(path)
            print("\n✅ Scan complete! Check detected_subs.json.")
        else:
            print("❌ Path not found.")
            
    elif choice == '2':
        service = input("Enter the service name (e.g., Adobe, Netflix): ")
        price = input("Enter current price: ")
        email_body = generate_email(service, price)
        print("\n--- 📧 Drafted Email ---\n")
        print(email_body)
        print("\n--- End of Draft ---")

    elif choice == '3':
        print("Stay vibey. Goodbye!")
        exit()

if __name__ == "__main__":
    while True:
        main_menu()