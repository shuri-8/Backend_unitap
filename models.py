from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    rfid = Column(String(50), unique=True, index=True, nullable=False)
    balance = Column(DECIMAL(12,2), default=0.00)
    status = Column(String(20), default="active")

    transactions = relationship("Transaction", back_populates="user")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(DECIMAL(12,2), nullable=False)
    txn_type = Column(String(10), nullable=False)  # debit/credit
    description = Column(String(255))
    timestamp = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="transactions")
