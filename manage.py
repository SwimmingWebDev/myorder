from db import db
from app import app
from models import Customer, Product, Order, ProductOrder
from sqlalchemy.sql import functions as func
import csv
import random

def drop_all_tables():
    db.drop_all()

def create_all_tables():
    db.create_all()

def import_data_from_CSV():
    
    with open("./data/customers.csv") as file:
        reader = csv.DictReader(file)
        customer_data = []
        for row in reader:
            customer_data.append(row)
        for customer in customer_data:
            new_customer = Customer(name=customer['name'], phone=customer['phone'])
            db.session.add(new_customer)
        db.session.commit()

    with open("./data/products.csv") as file:
        reader = csv.DictReader(file)
        product_data = []
        for row in reader:
            product_data.append(row)
    
        for product in product_data:
            new_product = Product(name=product['name'], price=product['price'])
            db.session.add(new_product)
        db.session.commit()

def randomize():
    # Find a random customer 
    cust_stmt = db.select(Customer).order_by(func.random()).limit(1) 
    customer = db.session.execute(cust_stmt).scalar() 
    
    # Make an order 
    order = Order(customer=customer) 
    db.session.add(order) 
    
    # Find a random product 
    prod_stmt = db.select(Product).order_by(func.random()).limit(1) 
    product = db.session.execute(prod_stmt).scalar() 
    rand_qty = random.randint(10, 20) 
    
    # Add that product to the order 
    association_1 = ProductOrder(order=order, product=product, quantity=rand_qty) 
    db.session.add(association_1) 
    
    # Do it again 
    prod_stmt = db.select(Product).order_by(func.random()).limit(1) 
    product = db.session.execute(prod_stmt).scalar() 
    rand_qty = random.randint(10, 20) 
    association_2 = ProductOrder(order=order, product=product, quantity=rand_qty) 
    db.session.add(association_2) 
    
    # Commit to the database 
    db.session.commit() 


def main():
    with app.app_context(): 
        drop_all_tables()
        create_all_tables()
        import_data_from_CSV()
        randomize()
        randomize()
        randomize()
        randomize()
        randomize()
        
if __name__ == "__main__":
    main()