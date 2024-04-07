from sqlalchemy import Boolean, Float, DateTime, Numeric, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from db import db
from sqlalchemy.sql import func
from datetime import datetime


class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False, unique=True)
    phone = mapped_column(String(50), nullable=False)
    balance = mapped_column(Numeric, nullable=False, default=0)
    orders = relationship("Order", back_populates="customer")
    
    def to_json(self):
        self.balance = round(self.balance, 2)
        return {
            "id":self.id,
            "name":self.name,
            "phone": self.phone,
            "balance": self.balance
        }

class Product(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False, unique=True)
    price = mapped_column(Numeric, nullable=False)
    available = mapped_column(Integer, nullable=False, default=0)
    product_items = relationship("ProductOrder", back_populates="product")

    def to_json(self):
        self.price = round(self.price, 2)
        return {
            "id":self.id,
            "name":self.name,
            "price": float(self.price),
            "available": self.available,
        }

class Order(db.Model):
    id = mapped_column(Integer, primary_key=True)
    customer_id = mapped_column(Integer, ForeignKey(Customer.id), nullable=False)
    customer = relationship("Customer", back_populates="orders")
    total = mapped_column(Numeric, nullable=False, default=0)
    items = relationship("ProductOrder", back_populates="order", cascade="all, delete-orphan")
    created = mapped_column(DateTime(timezone=True), default=datetime.now().replace(microsecond=0))
    processed = mapped_column(DateTime(timezone=True), nullable=True)
    
    def calculate_total(self, list):
        return {
            round(sum(list), 2)
        }
    
    def to_json(self):
        return {
            "id":self.id,
            "customer_id":self.customer_id,
            "created": self.created,
            "processed": self.processed,
        }
        
    def process(self, strategy):  
            if self.processed is None:
                if self.customer.balance > 0:  
                    self.total = 0 
                    for item in self.items:
                        if item.quantity > item.product.available:
                            if strategy == "ignore":
                                item.quantity = 0
                            elif strategy == "reject":
                                return "Insufficient Quantity", False
                            else:
                                strategy = "adjust"
                                item.quantity = item.product.available    
                        item.product.available -= item.quantity
                        sub_total = 0   
                        sub_total += (float(item.product.price) * float(item.quantity))
                        if sub_total > self.customer.balance:
                            return "Insufficient Balance", False
                        self.total += sub_total
                    self.customer.balance = float(self.customer.balance)
                    self.customer.balance -= self.total
                    self.processed = func.now()
                    return True
            else:
                return "Invalid Value", 400


class ProductOrder(db.Model):
    id = mapped_column(Integer, primary_key=True)
    order_id = mapped_column(Integer, ForeignKey(Order.id))
    order = relationship("Order", back_populates="items")
    product_id = mapped_column(Integer, ForeignKey(Product.id), nullable=False)
    product = relationship("Product", back_populates="product_items")
    quantity = mapped_column(Integer, nullable=False, default=0)
