from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from db import db

class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False, unique=True)
    phone = mapped_column(String(50), nullable=False)
    balance = mapped_column(Numeric, nullable=False, default=0)
    
    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "phone": self.phone,
            "balance": self.balance,
        }

class Product(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False, unique=True)
    price = mapped_column(Integer)
    available = mapped_column(Integer, nullable=False, default=0)

    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "price": self.price,
            "available": self.available,
        }

