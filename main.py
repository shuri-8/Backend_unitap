from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import database, models, schemas, crud

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="RFID Wallet Backend")

@app.post("/validate_rfid", response_model=schemas.ValidateRFIDResponse)
def validate_rfid(request: schemas.ValidateRFIDRequest, db: Session = Depends(database.get_db)):
    user = crud.get_user_by_rfid(db, request.rfid)
    if not user:
        return {"valid": False, "message": "RFID not valid or inactive"}
    return {"valid": True, "user_name": user.name, "message": "RFID is valid and active"}

@app.get("/get_balance", response_model=schemas.BalanceResponse)
def get_balance(rfid: str, db: Session = Depends(database.get_db)):
    balance = crud.get_balance(db, rfid)
    if balance is None:
        raise HTTPException(status_code=404, detail="RFID not found")
    return {"balance": float(balance)}

@app.post("/log_transaction", response_model=schemas.TransactionResponse)
def log_transaction(request: schemas.TransactionRequest, db: Session = Depends(database.get_db)):
    result = crud.log_transaction(db, request.rfid, request.amount, request.txn_type, request.description)
    if not result:
        raise HTTPException(status_code=400, detail="Transaction failed (invalid RFID or insufficient balance)")
    txn, new_balance = result
    return {"status": "success", "transaction_id": txn.id, "new_balance": float(new_balance)}

@app.get("/get_transaction_history", response_model=list[schemas.TransactionHistoryResponse])
def get_transaction_history(rfid: str, limit: int = 10, db: Session = Depends(database.get_db)):
    history = crud.get_transaction_history(db, rfid, limit)
    return history
