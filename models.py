from sqlalchemy import Boolean, Float, DateTime, Numeric, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from db import db
from sqlalchemy.sql import func

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
            "price": self.price,
            "available": self.available,
        }

class Order(db.Model):
    id = mapped_column(Integer, primary_key=True)
    customer_id = mapped_column(Integer, ForeignKey(Customer.id), nullable=False)
    customer = relationship("Customer", back_populates="orders")
    total = mapped_column(Numeric)
    items = relationship("ProductOrder", back_populates="order", cascade="all, delete-orphan")
    date_created = mapped_column(DateTime(timezone=True), default=func.now())
    processed = mapped_column(DateTime(timezone=True), nullable=True)
    
    def calculate_total(self, list):
        return {
            round(sum(list), 2)
        }
    
    # def product_to_dict(self, name, quantity):
    #     items = []
    #     item = {
    #         "name": name,
    #         "quantity":quantity
    #     }
    #     return items.push(item)
        
    # def process(self, strategy="adjust"):
    #     if (self.processed is not None) and (self.customer.balance > 0):
    #         if self.order.quantity > self.order.product.available:
    #             strategy="adjust"




class ProductOrder(db.Model):
    id = mapped_column(Integer, primary_key=True)
    order_id = mapped_column(Integer, ForeignKey(Order.id))
    order = relationship("Order", back_populates="items")
    product_id = mapped_column(Integer, ForeignKey(Product.id), nullable=False)
    product = relationship("Product", back_populates="product_items")
    quantity = mapped_column(Integer, nullable=False, default=0)
