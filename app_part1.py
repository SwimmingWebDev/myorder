from pathlib import Path
from flask import Flask, render_template, redirect, url_for
from models import Customer, Product
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myorder.db"
app.instance_path = Path("data").resolve()

db.init_app(app)

@app.route("/")
def home():
    return redirect(url_for('customer_list'))

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

