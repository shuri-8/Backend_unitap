# RFID Wallet Backend

FastAPI + MySQL backend for handling RFID-based transactions.

## Features
- Validate RFID
- Get balance
- Log debit/credit transaction
- Get transaction history

## Run locally
1. Create MySQL DB and set `.env`
2. Install dependencies
3. Run: `uvicorn app.main:app --reload`
4. Open: http://127.0.0.1:8000/docs
