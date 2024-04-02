from flask import Blueprint, jsonify, request
from db import db 
from models import Customer, Product, ProductOrder, Order

api_orders_bp = Blueprint("api_orders", __name__)

# create Order   
@api_orders_bp.route("/", methods=["GET", "POST"])
def api_create_order():
    if request.method == 'POST':
        data = request.json

        customer_id = data["customer_id"]
        items = data.get('items', [])

        customer = db.get_or_404(Customer, customer_id)
        order = Order(customer=customer)

        for item in items:
            name = item.get("name")
            quantity = item.get('quantity')

            if not isinstance(quantity, int):
                return "Invalid request", 400
            
            product = Product.query.filter_by(name=name).first_or_404()
          
            print(product)
            if product is not None:
                new_order = ProductOrder(order=order, product=product, quantity=quantity) 
                db.session.add(new_order)
            db.session.commit()

        return "Created Successfully", 201
    else:
        statement = db.select(Order).order_by(Order.id)
        results = db.session.execute(statement)
        orders = []
        for order in results.scalars():
            json_record =Order.to_json(order)
            orders.append(json_record)
        return jsonify(orders)

# Update order
@api_orders_bp.route("/<int:order_id>", methods=["PUT"])
def api_process_order(order_id):
    order= db.get_or_404(Order, order_id)
    data = request.json

    if data["process"] == True:
        if data["strategy"]:
            Order.process(order, data["strategy"])
            db.session.commit()    
        else:
            data["strategy"]="adjust"
            Order.process(order, data["strategy"])
            db.session.commit() 
        return "", 204

    else:
        return "Invalid request", 400
     
# delete order
@api_orders_bp.route("/delete/<int:order_id>", methods=["DELETE"])
def api_delete_order(order_id):
    order = db.get_or_404(Order, order_id)
    db.session.delete(order)
    db.session.commit()
    return "", 204