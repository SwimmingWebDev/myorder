from pathlib import Path
from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import Customer, Product, Order, ProductOrder
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myorder.db"
app.instance_path = Path("data").resolve()

db.init_app(app)

@app.route("/")
def home():
    return redirect(url_for('customers_list'))


# Create customer
@app.route("/api/customers", methods=['POST', 'GET'])
def customers_list():
    if request.method == 'POST':

        name = request.form['name']
        phone =request.form['phone']
        new_customer = Customer(name=name, phone=phone)

        db.session.add(new_customer)
        db.session.commit()
        return redirect("/api/customers")
    
    else:
        statement = db.select(Customer).order_by(Customer.name)
        results = db.session.execute(statement)
        customers = []
        for customer in results.scalars():
            json_record = Customer.to_json(customer)
            customers.append(json_record)
        return render_template("customers.html", customers = customers)

# Update customer
@app.route("/api/customers/<int:customer_id>", methods=["GET", "POST"])
def update_customer(customer_id):
    customer = db.get_or_404(Customer, customer_id)
 
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.phone =request.form['phone']

        db.session.commit()
        return redirect('/')

    else:
        return render_template('update_customer.html', customer = customer)

# Delete Customer
@app.route("/api/customers/delete/<int:customer_id>")
def customer_delete(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return redirect('/')

@app.route("/products")
def products_list():
    statement = db.select(Product).order_by(Product.name)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("products.html", products = results)

@app.route("/orders")
def orders_list():
    statement = db.select(Order).order_by(Order.id)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("orders.html", orders = results)

# Create Orders
@app.route("/api/orders/<int:customer_id>", methods=["POST"])
def get_orders(customer_id):
    customer = db.get_or_404(Customer, customer_id)



# @app.route("/customers")
# def customer_list(): 
#     statement = db.select(Customer).order_by(Customer.name)
#     records = db.session.execute(statement)
#     results = records.scalars()
#     return render_template("customers.html", customers = results)

# JSON
# @app.route("/api/customers/<int:customer_id>", methods=["GET"])
# def customer_detail_json(customer_id):
#     statement = db.select(Customer).where(Customer.id == customer_id)
#     result = db.session.execute(statement)
#     customer_detail = []
#     for customer in result.scalars():
#         json_record = Customer.to_json(customer)
#         customer_detail.append(json_record)
#     return jsonify(customer_detail)


if __name__ == "__main__":
    app.run(debug=True, port=8888)


#api delete url could not be the same as update url
#name could not be shown full name