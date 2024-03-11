from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from db import db

class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False, unique=True)
    phone = mapped_column(String(50), nullable=False)
    balance = mapped_column(Numeric, nullable=False, default=0)
    orders = relationship("Order", back_populates="customer")
    
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
    product_items = relationship("ProductOrder", back_populates="items")

    def to_json(self):
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
    total = mapped_column(Numeric, nullable=True)
    order_list = relationship("ProductOrder", back_populates="order")

    def to_json(self):
        return {
            "id":self.id,
            "customer_id":self.customer_id,
            "customer": self.customer,
            "total": self.total,
        }
    
    def calculate_total(self, list):
        return {
            round(sum(list), 2)
        }

class ProductOrder(db.Model):
    id = mapped_column(Integer, primary_key=True)
    order_id = mapped_column(Integer, ForeignKey(Order.id), nullable=False)
    order = relationship("Order", back_populates="order_list")
    product_id = mapped_column(Integer, ForeignKey(Product.id), nullable=False)
    items = relationship("Product", back_populates="product_items")
    quantity = mapped_column(Integer, nullable=False, default=0)

    def to_json(self):
        return {
            "id":self.id,
            "order_id":self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
        }