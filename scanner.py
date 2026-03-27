import os
import re
import json

# Known subscription services to try to identify from file content
KNOWN_SERVICES = [
    "netflix", "spotify", "adobe", "hulu", "disney", "apple", "amazon",
    "youtube", "microsoft", "google", "dropbox", "slack", "zoom", "github",
    "notion", "figma", "canva", "lastpass", "nordvpn", "expressvpn",
    "duolingo", "headspace", "calm", "grammarly", "audible", "kindle",
]

# Fix: require '$' sign to avoid matching version numbers, IDs, etc.
PRICE_PATTERN = re.compile(r'\$\s?\d{1,4}(?:,\d{3})*(?:\.\d{2})?')

SUPPORTED_EXTENSIONS = (".txt", ".eml", ".html", ".htm")


def extract_service_name(content: str, filename: str) -> str:
    """Try to identify the subscription service from content or filename."""
    content_lower = content.lower()
    filename_lower = filename.lower()

    for service in KNOWN_SERVICES:
        if service in content_lower or service in filename_lower:
            return service.capitalize()

    # Fall back to filename stem (without extension) as a hint
    stem = os.path.splitext(filename)[0]
    if stem:
        return stem.replace("_", " ").replace("-", " ").title()

    return "Unknown Service"


def scan_files(directory: str):
    matches = []
    seen_services = set()  # Deduplication by service name

    print(f"🔍 Scanning directory: {directory}")

    try:
        entries = os.listdir(directory)
    except PermissionError:
        print(f"❌ Permission denied: {directory}")
        return

    for filename in entries:
        if not filename.endswith(SUPPORTED_EXTENSIONS):
            continue

        print(f"📄 Checking: {filename}")
        filepath = os.path.join(directory, filename)

        try:
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read()
        except OSError as e:
            print(f"  ⚠️  Could not read {filename}: {e}")
            continue

        content_lower = content.lower()

        # Look for subscription keywords AND a properly-formatted price
        has_sub_keyword = any(kw in content_lower for kw in ("subscription", "billing", "renewal", "recurring", "charged"))
        price_match = PRICE_PATTERN.search(content)

        if has_sub_keyword and price_match:
            price = price_match.group().strip()
            service = extract_service_name(content, filename)

            # Fix: skip duplicate services
            if service in seen_services:
                print(f"  ⚠️  Duplicate skipped: {service} already recorded.")
                continue

            seen_services.add(service)
            matches.append({
                "file": filename,
                "service": service,
                "price": price,
            })
            print(f"✅ MATCH: {service} @ {price} (from {filename})")

    if matches:
        with open('detected_subs.json', 'w') as j:
            json.dump(matches, j, indent=4)
        print(f"\n🎉 Saved {len(matches)} subscription(s) to detected_subs.json")
    else:
        print("\n❌ No subscriptions found. Make sure files contain billing keywords and a $ price.")


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    scan_files(path)
