from flask import Blueprint, jsonify, request
from db import db 
from models import Product

api_products_bp = Blueprint("api_products", __name__)

# Create product 
@api_products_bp.route("/", methods=['GET', 'POST' ])
def api_create_product():
    if request.method == 'POST':
        data = request.json
        
        if "name" not in data:
            return "Invalid request", 400
        if "price" not in data or data["price"] < 0:
            return "Invalid request", 400
        
        name = data["name"]
        price = data["price"]
        
        new_product = Product(name=name, price=price)
        db.session.add(new_product)

        db.session.commit()
        return "Created Successfully", 201
    else:
        statement = db.select(Product).order_by(Product.id)
        results = db.session.execute(statement)
        products = []
        for product in results.scalars():
            json_record = Product.to_json(product)
            products.append(json_record)
        return jsonify(products)
      
# Update product
@api_products_bp.route("/<int:product_id>", methods=["PUT"])
def api_update_product(product_id):
    product = db.get_or_404(Product, product_id)
 
    if request.method == 'PUT':
        data = request.json
        if "name" not in data:
            return "Invalid request", 400
        
        if data["price"] < 0 or not isinstance(data["price"], float):
            return "Invalid request", 400
        
        if not isinstance(data["available"], int):
            return "Invalid request", 400

        product.name = data['name']
        product.price = data['price']
        product.available =data['available']

        db.session.commit()
        return "", 204

# Delete product
@api_products_bp.route("/delete/<int:product_id>", methods=['DELETE'] )
def api_delete_product(product_id):
    product = db.get_or_404(Product, product_id)
    db.session.delete(product)
    db.session.commit()
    return "", 204
