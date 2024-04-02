from flask import Blueprint, request, redirect, render_template, url_for
from db import db 
from models import Customer, Order, Product, ProductOrder

orders_bp = Blueprint("orders", __name__)


# list orders
@orders_bp.route("/", methods=['GET', 'POST'])
def orders_list():
        statement = db.select(Order).order_by(Order.id)
        records = db.session.execute(statement)
        results = records.scalars()
        return render_template("orders.html", orders = results)

# create order
@orders_bp.route("/new", methods=['GET', 'POST'])
def make_order():
    if request.method == 'POST':
        customer_id = request.form['customer']
        
        customer = db.get_or_404(Customer, customer_id)
        order = Order(customer=customer)
        
        for i in range(1,4):
            product_id = request.form.get(f'item_{i}')
            product = db.get_or_404(Product, product_id)

            quantity = request.form.get(f'quantity_{i}')
    
            new_order = ProductOrder(order=order, product=product, quantity=quantity) 
            db.session.add(new_order) 
            db.session.commit()

        return redirect(url_for("orders.orders_list"))
  
    else:
        statement1 = db.select(Customer).order_by(Customer.id)
        records1 = db.session.execute(statement1)
        customers = records1.scalars()

        statement2 = db.select(Product).order_by(Product.id)
        records2 = db.session.execute(statement2)
        products1 = records2.scalars()

        statement3 = db.select(Product).order_by(Product.id)
        records3 = db.session.execute(statement3)
        products2 = records3.scalars()

        statement4 = db.select(Product).order_by(Product.id)
        records4 = db.session.execute(statement4)
        products3 = records4.scalars()


        return render_template("make_order.html", customers = customers, products1=products1, products2=products2,  products3=products3)

# list singl order details
@orders_bp.route("/<int:order_id>")
def order_details(order_id):
    statement = db.select(ProductOrder).filter_by(order_id=order_id)
    records = db.session.execute(statement)
    results = records.scalars()
    order = db.get_or_404(Order, order_id)
    return render_template("order_details.html", total = order.total, orders = results, order_id = order_id)

# update order
@orders_bp.route("/process/<int:order_id>", methods=["GET","POST"])
def process_order(order_id):
    order= db.get_or_404(Order, order_id)
    strategy = request.form['strategy']
    Order.process(order, strategy)
    db.session.commit()
    return redirect(url_for("orders.orders_list"))
    
# delete order
@orders_bp.route("/<int:order_id>/delete", methods=["GET", "POST"])
def order_delete(order_id):
    order = db.get_or_404(Order, order_id)
    if order.processed is not None:
        return redirect(url_for("orders.orders_list"))
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("orders.orders_list"))

