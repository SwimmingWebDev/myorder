from sqlalchemy import Boolean, Float, DateTime, Numeric, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from db import db
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
    price = mapped_column(Integer, nullable=False)
    quantity = mapped_column(Integer, nullable=False, default=0)
    product_items = relationship("ProductOrder", back_populates="product")

    def to_json(self):
        self.price = round(self.price, 2)
        return {
            "id":self.id,
            "name":self.name,
            "price": self.price,
            "quantity": self.quantity,
        }

class Order(db.Model):
    id = mapped_column(Integer, primary_key=True)
    customer_id = mapped_column(Integer, ForeignKey(Customer.id), nullable=False)
    customer = relationship("Customer", back_populates="orders")
    total = mapped_column(Numeric, nullable=True)
    items = relationship("ProductOrder", back_populates="order")
    date_ordered = mapped_column(DateTime, default=datetime.utcnow)

    def to_json(self):
        return {
            "id":self.id,
            "customer_id":self.customer_id,
            "items":self.items,
            "date_ordered":self.date_ordered
        }
    
    def calculate_total(self, list):
        return {
            round(sum(list), 2)
        }

class ProductOrder(db.Model):
    id = mapped_column(Integer, primary_key=True)
    order_id = mapped_column(Integer, ForeignKey(Order.id), nullable=False)
    order = relationship("Order", back_populates="items")
    product_id = mapped_column(Integer, ForeignKey(Product.id), nullable=False)
    product = relationship("Product", back_populates="product_items")
    quantity = mapped_column(Integer, nullable=False, default=0)

    def to_json(self):
        return {
            "id":self.id,
            "order_id":self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
        }