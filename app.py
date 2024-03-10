from pathlib import Path
from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import Customer, Product
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myorder.db"
app.instance_path = Path("data").resolve()

db.init_app(app)

@app.route("/")
def home():
    return redirect(url_for('customer_list'))

@app.route("/api/customers")
def customers_json():
    statement = db.select(Customer).order_by(Customer.name)
    results = db.session.execute(statement)
    customers = []
    for customer in results.scalars():
        json_record = {
            "id" : customer.id,
            "name" : customer.name,
            "phone" : customer.phone,
            "balance" : customer.balance,
        }
        customers.append(json_record)
    return jsonify(customers)


@app.route("/api/customers/<int:customer_id>", methods=['GET'])
def customer_detail_json(customer_id):
    statement = db.select(Customer).where(Customer.id == customer_id)
    result = db.session.execute(statement)
    customer_detail = []
    for customer in result.scalars():
        json_record = {
            "id" : customer.id,
            "name" : customer.name,
            "phone" : customer.phone,
            "balance" : customer.balance,
        }
        customer_detail.append(json_record)
    return jsonify(customer_detail)

@app.route("/api/customers/<int:customer_id>", methods=["DELETE"])
def customer_delte(customer_id):
    customer = db.session.execute(db.select(Customer).where(Customer.id == customer_id))
    db.session.delete(customer)
    db.session.commit()
    return f"Customer id: {customer_id} has been deleted"


@app.route("/example", methods=["POST"])
def example():
    print(request.json)

# return a specific HTTP error code
@app.route("/example/<int:customer_id>", methods=["POST"])
def update_customer(customer_id):
    data = request.json
    customer = db.get_or_404(Customer, customer_id)

    if "balance" not in data:
        return "Invalid request", 400
    
    balance = data["balance"]
    if not isinstance(balance, [int, float]):
        return "Invalid request: balance", 400
    customer.balance = balance

    db.session.commit()
    return "",204

@app.route("/customers")
def customer_list(): 
    statement = db.select(Customer).order_by(Customer.name)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("customers.html", customers = results)

@app.route("/products")
def product_list():
    statement = db.select(Product).order_by(Product.name)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("products.html", products = results)

if __name__ == "__main__":
    app.run(debug=True, port=8888)

