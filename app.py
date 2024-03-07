from pathlib import Path
from flask import Flask, render_template
from db import db
import csv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///purchase.db"
app.instance_path = Path("data").resolve()

db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/customers")
def customer_list():
    with open("./data/customers.csv") as file:
        reader = csv.DictReader(file)
        my_data = []
        for row in reader:
            my_data.append(row)

    return render_template("customers.html", customers = my_data)

@app.route("/products")
def product_list():
    with open("./data/products.csv") as file:
        reader = csv.DictReader(file)
        my_data = []
        for row in reader:
            my_data.append(row)

    return render_template("products.html", products = my_data)


if __name__ == "__main__":
    app.run(debug=True, port=8888)

