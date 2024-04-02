from flask import Flask, url_for, redirect
from pathlib import Path
from db import db

from routes import api_customers_bp, api_products_bp, api_orders_bp
from routes import customers_bp, products_bp, orders_bp

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myorder.db"

app.instance_path = Path("data").resolve()

db.init_app(app)

# API
app.register_blueprint(api_customers_bp, url_prefix="/api/customers")
app.register_blueprint(api_products_bp, url_prefix="/api/products")
app.register_blueprint(api_orders_bp, url_prefix="/api/orders")

# homepage
@app.route("/")
def home():
    return redirect(url_for("customers.customers_list"))

# view
app.register_blueprint(customers_bp, url_prefix="/customers")
app.register_blueprint(products_bp, url_prefix="/products")
app.register_blueprint(orders_bp, url_prefix="/orders")


if __name__ == "__main__":
    app.run(debug=True, port=8888)
