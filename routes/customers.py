from flask import Blueprint, request, redirect, render_template
from db import db 
from models import Customer, Order

customers_bp = Blueprint("customers", __name__)

# Create customer
@customers_bp.route("/", methods=['GET', 'POST'])
def customers_list():
    if request.method == 'POST':

        name = request.form['name']
        phone =request.form['phone']
        new_customer = Customer(name=name, phone=phone)

        db.session.add(new_customer)
        db.session.commit()
        return redirect("/")
    
    else:
        statement = db.select(Customer).order_by(Customer.id)
        results = db.session.execute(statement)
        customers = []
        for customer in results.scalars():
            json_record = Customer.to_json(customer)
            customers.append(json_record)

        return render_template("customers.html", customers = customers)

# Update customer
@customers_bp.route("/update/<int:customer_id>", methods=["GET", "POST"])
def update_customer(customer_id):

    customer = db.get_or_404(Customer, customer_id)
 
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.phone =request.form['phone']
        customer.balance = request.form['balance']
        
        db.session.commit()
        return redirect("/")
    else:
        json_record = Customer.to_json(customer)
        return render_template('update_customer.html', customer = json_record )

# Delete Customer
@customers_bp.route("/delete/<int:customer_id>")
def customer_delete(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return redirect('/')

# all orders associated with the customer
@customers_bp.route("/<int:customer_id>")
def customer_order(customer_id):
    statement = db.select(Order).filter_by(customer_id=customer_id)
    results = db.session.execute(statement)
    
    orders = []
    for order in results.scalars():
        json_record = Order.to_json(order)
        orders.append(json_record)
    return render_template("customer_orders.html", orders = orders)

