from flask import Blueprint, request, url_for, redirect, render_template
from db import db 
from models import Product

products_bp = Blueprint("products", __name__)

# create product
@products_bp.route("/", methods=['GET', 'POST'])
def products_list():
    if request.method == 'POST':

        name = request.form['name']
        price =request.form['price']
        new_product = Product(name=name, price=price)

        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("products.products_list"))
    
    else:
        statement = db.select(Product).order_by(Product.id)
        results = db.session.execute(statement)
        products = []
        for product in results.scalars():
            json_record = Product.to_json(product)
            products.append(json_record)

        return render_template("products.html", products = products)

# Update product
@products_bp.route("/<int:product_id>", methods=["GET", "POST"])
def update_product(product_id):

    product = db.get_or_404(Product, product_id)
 
    if request.method == 'POST':
        product.name = request.form['name']
        product.price =request.form['price']
        product.available = request.form['available']
        
        db.session.commit()
        return redirect(url_for("products.products_list"))
    else:
        json_record = Product.to_json(product)
        return render_template('update_product.html', product = json_record )

# Delete product
@products_bp.route("/delete/<int:product_id>")
def delete_product(product_id):
    product = db.get_or_404(Product, product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("products.products_list"))

