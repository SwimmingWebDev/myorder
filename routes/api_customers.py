from flask import Blueprint, jsonify, request
from db import db 
from models import Customer

api_customers_bp = Blueprint("api_customers", __name__)

# Create customer 
@api_customers_bp.route("/", methods=['GET', 'POST'])
def api_create_customer():
    
    if request.method == 'POST':
        data = request.json
        
        if "name" not in data:
            return "Invalid request", 400
        if "phone" not in data:
            return "Invalid request", 400
        
        name = data["name"]
        phone = data["phone"]
        
        new_customer = Customer(name=name, phone=phone)
        db.session.add(new_customer)

        db.session.commit()
        return "Created Successfully", 201
    else:
        statement = db.select(Customer).order_by(Customer.id)
        results = db.session.execute(statement)
        customers = []
        for customer in results.scalars():
            json_record = Customer.to_json(customer)
            customers.append(json_record)
        return jsonify(customers)
       
# Update customer
@api_customers_bp.route("/<int:customer_id>", methods=["PUT"])
def api_update_customer(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    
    if request.method == 'PUT':
        data = request.json
        if "balance" not in data:
            return "Invalid request", 400
        customer.balance = data['balance']

        if not isinstance(customer.balance, (int, float)):
            return "Invalid request", 400
        
        customer.name = data['name']
        customer.phone = data['phone']

        db.session.commit()
        return "", 204

# Delete Customer
@api_customers_bp.route("/delete/<int:customer_id>", methods=['DELETE'] )
def api_delete_customer(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return "", 204