import json
import re
import sys
from pathlib import Path
from datetime import datetime

DB = "detected_subs.json"
JUNK = ['advertisement', 'promo', 'marketing']

def load_db():
    return json.load(open(DB)) if Path(DB).exists() else []

def extract(line):
    """Returns (skip_bool, price, service)"""
    low = line.lower()
    if any(bad in low for bad in JUNK):
        return True, None, None
    
    # Price: $ followed by digits/decimal
    p = re.search(r'\$\s*[\d,]+\.?\d{0,2}', line)
    price = p.group(0).replace(' ', '') if p else None
    
    # Service: word before 'Subscription'
    service = None
    if 'subscription' in low:
        words = line.split()
        for i, w in enumerate(words):
            if 'subscription' in w.lower() and i > 0:
                service = words[i-1].strip('.,:;[]')
                break
    
    return False, price, service

def scan(directory="."):
    existing = load_db()
    seen = {(e["file"], e["line"], e["text"]) for e in existing}
    new_entries = []
    
    for pat in ['*.txt', '*.eml']:
        for fp in Path(directory).glob(pat):
            try:
                with open(fp, 'r', errors='ignore') as f:
                    for num, line in enumerate(f, 1):
                        if '$' not in line or not any(k in line.lower() for k in ['subscription','renew']):
                            continue
                        
                        skip, price, service = extract(line)
                        if skip:
                            print(f"- {fp.name}:{num} (junk)")
                            continue
                        
                        entry = {
                            "file": str(fp),
                            "line": num,
                            "service": service,
                            "price": price,
                            "text": line.strip(),
                            "found": datetime.now().isoformat()
                        }
                        key = (entry["file"], entry["line"], entry["text"])
                        if key not in seen:
                            new_entries.append(entry)
                            print(f"+ {service or 'Unknown'} @ {price or '?'}")
                        else:
                            print(f"= {fp.name}:{num} (dup)")
            except Exception as e:
                print(f"! {fp}: {e}", file=sys.stderr)
    
    if new_entries:
        with open(DB, 'w') as f:
            json.dump(existing + new_entries, f, indent=2)
        print(f"\n>> Added {len(new_entries)} clean subs")

if __name__ == "__main__":
    scan(sys.argv[1] if len(sys.argv) > 1 else ".")
