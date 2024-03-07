from db import db
from app import app
from models import Customer, Product
import csv

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

def main():
    with app.app_context(): 
        drop_all_tables()
        create_all_tables()
        import_data_from_CSV()
        

if __name__ == "__main__":
    main()