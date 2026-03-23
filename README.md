# SubVibe 📱

**SubVibe** is a lightweight, privacy-focused subscription auditor and negotiator built entirely on Android. It helps you find hidden "digital entropy" in your inbox and provides the templates to negotiate better rates.

## 🚀 Built with the "Vibe Coding" Stack
This project is a testament to the power of mobile development in 2026:
* **Brain:** Kimi K2.5 (Logic & Code Generation)
* **Environment:** Termux (Python 3.x)
* **Editor:** Acode / MT Manager
* **Git Client:** MGit (Open Source)

## ✨ Features
* **Zero-Cloud Parsing:** Scans local `.eml` or `.txt` receipt exports without uploading your data to a server.
* **Waste Detection:** Identifies duplicate services or "ghost" subscriptions.
* **Negotiation Engine:** AI-optimized templates for student discounts and retention offers.

## 🛠️ Installation (Android/Termux)
```bash
pkg install python
git clone https://github.com/GGWarrior001/SubVibe.git
cd SubVibe
pip install -r requirements.txt
python main.py

## How to use:
1. Run `python scanner.py [path_to_your_receipts]` to find subscriptions.
2. Run `python negotiate.py` to generate the negotiation emails.
