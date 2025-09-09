from sqlalchemy.orm import Session
from . import models

def get_user_by_rfid(db: Session, rfid: str):
    return db.query(models.User).filter(models.User.rfid == rfid, models.User.status == "active").first()

def get_balance(db: Session, rfid: str):
    user = get_user_by_rfid(db, rfid)
    return user.balance if user else None

def log_transaction(db: Session, rfid: str, amount: float, txn_type: str, description: str = None):
    user = get_user_by_rfid(db, rfid)
    if not user:
        return None

    if txn_type == "debit" and user.balance < amount:
        return None

    if txn_type == "debit":
        user.balance -= amount
    elif txn_type == "credit":
        user.balance += amount

    txn = models.Transaction(user_id=user.id, amount=amount, txn_type=txn_type, description=description)
    db.add(txn)
    db.commit()
    db.refresh(txn)
    db.refresh(user)
    return txn, user.balance

def get_transaction_history(db: Session, rfid: str, limit: int = 10):
    user = get_user_by_rfid(db, rfid)
    if not user:
        return []
    return db.query(models.Transaction).filter(models.Transaction.user_id == user.id).order_by(models.Transaction.timestamp.desc()).limit(limit).all()
