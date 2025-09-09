from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ValidateRFIDRequest(BaseModel):
    rfid: str

class ValidateRFIDResponse(BaseModel):
    valid: bool
    user_name: Optional[str] = None
    message: str

class BalanceResponse(BaseModel):
    balance: float

class TransactionRequest(BaseModel):
    rfid: str
    amount: float
    txn_type: str
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    status: str
    transaction_id: int
    new_balance: float

class TransactionHistoryResponse(BaseModel):
    id: int
    amount: float
    txn_type: str
    description: Optional[str]
    timestamp: datetime
