import os
import re
import json

def scan_files(directory):
    matches = []
    # This looks for an optional $, then numbers, then a decimal
    price_pattern = r"\$?\s?\d+(?:\.\d{2})?"

    
    print(f"🔍 Scanning directory: {directory}")
    
    for filename in os.listdir(directory):
        # We check all files that aren't Python scripts or JSON
        if filename.endswith(".txt") or filename.endswith(".eml"):
            print(f"📄 Checking: {filename}")
            filepath = os.path.join(directory, filename)
            
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read().lower()
                # Look for 'sub' AND a price in the same file
                if 'sub' in content and re.search(price_pattern, content):
                    price = re.search(price_pattern, content).group()
                    matches.append({
                        "file": filename,
                        "service": "Found Subscription",
                        "price": price
                    })
                    print(f"✅ MATCH FOUND in {filename}!")

    if matches:
        with open('detected_subs.json', 'w') as j:
            json.dump(matches, j, indent=4)
        print(f"\n🎉 Success! Saved {len(matches)} matches to detected_subs.json")
    else:
        print("\n❌ No subscriptions found. Check your file content!")

if __name__ == "__main__":
    import sys
    # Use current folder if no path given
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    scan_files(path)
    