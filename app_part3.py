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
@app.route("/customers", methods=['GET', 'POST'])
def customers_list():
    if request.method == 'POST':

        name = request.form['name']
        phone =request.form['phone']
        new_customer = Customer(name=name, phone=phone)

        db.session.add(new_customer)
        db.session.commit()
        return redirect("/customers")
    
    else:
        statement = db.select(Customer).order_by(Customer.id)
        results = db.session.execute(statement)
        customers = []
        for customer in results.scalars():
            json_record = Customer.to_json(customer)
            customers.append(json_record)

        return render_template("customers.html", customers = customers)

# Update customer
@app.route("/customer/update/<int:customer_id>", methods=["GET", "POST"])
def update_customer(customer_id):

    customer = db.get_or_404(Customer, customer_id)
 
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.phone =request.form['phone']
        customer.balance = request.form['balance']
        
        db.session.commit()
        return redirect("/customers")
    else:
        json_record = Customer.to_json(customer)
        return render_template('update_customer.html', customer = json_record )

# Delete Customer
@app.route("/customer/delete/<int:customer_id>")
def customer_delete(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return redirect('/')

# all orders associated with the customer
@app.route("/customer/<int:customer_id>")
def customer_order(customer_id):
    statement = db.select(Order).filter_by(customer_id=customer_id)
    results = db.session.execute(statement)
    
    orders = []
    for order in results.scalars():
        json_record = Order.to_json(order)
        orders.append(json_record)
    return render_template("customer_orders.html", orders = orders)

# API view - customer
# Create customer 
@app.route("/api/customers", methods=['POST', 'GET'])
def api_create_customer():
    if request.method == 'GET':
        statement = db.select(Customer).order_by(Customer.id)
        results = db.session.execute(statement)
        customers = []
        for customer in results.scalars():
            json_record = Customer.to_json(customer)
            customers.append(json_record)
        return jsonify(customers)
    
    if request.method == 'POST':
        data = request.json
        
        if "name" not in data:
            return "Invalid request", 400
        if "phone" not in data:
            return "Invalid request", 400
        
        name = data["name"]
        phone = data["phone"]
        
        new_customer = Customer(name=name, phone=phone)
        db.session.add(new_customer)

        db.session.commit()
        return "Created Successfully", 201
# API view - customer    
# Update customer
@app.route("/api/customer/<int:customer_id>", methods=["GET", "PUT"])
def api_update_customer(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    
    if request.method == 'PUT':
        data = request.json
        if "balance" not in data:
            return "Invalid request", 400
        customer.balance = data['balance']

        if not isinstance(customer.balance, (int, float)):
            return "Invalid request", 400
        
        customer.name = data['name']
        customer.phone =data['phone']

        db.session.commit()
        return "", 204

    else:
        return render_template('update_customer.html', customer = customer)
# API view - customer
# Delete Customer
@app.route("/api/customer/delete/<int:customer_id>", methods=['DELETE'] )
def api_delete_customer(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return "", 204

# create product
@app.route("/products", methods=['GET', 'POST'])
def products_list():
    if request.method == 'POST':

        name = request.form['name']
        price =request.form['price']
        new_product = Product(name=name, price=price)

        db.session.add(new_product)
        db.session.commit()
        return redirect("/products")
    
    else:
        statement = db.select(Product).order_by(Product.id)
        results = db.session.execute(statement)
        products = []
        for product in results.scalars():
            json_record = Product.to_json(product)
            products.append(json_record)

        return render_template("products.html", products = products)

# Update product
@app.route("/product/<int:product_id>", methods=["GET", "POST"])
def update_product(product_id):

    product = db.get_or_404(Product, product_id)
 
    if request.method == 'POST':
        product.name = request.form['name']
        product.price =request.form['price']
        product.available = request.form['available']
        
        db.session.commit()
        return redirect("/products")
    else:
        json_record = Product.to_json(product)
        return render_template('update_product.html', product = json_record )

# Delete product
@app.route("/product/delete/<int:product_id>")
def delete_product(product_id):
    product = db.get_or_404(Product, product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/products')


# API view - product
# Create product 
@app.route("/api/products", methods=['GET', 'POST' ])
def api_create_product():
    if request.method == 'GET':
        statement = db.select(Product).order_by(Product.id)
        results = db.session.execute(statement)
        products = []
        for product in results.scalars():
            json_record = Product.to_json(product)
            products.append(json_record)
        return jsonify(products)
    
    if request.method == 'POST':
        data = request.json
        
        if "name" not in data:
            return "Invalid request", 400
        if "price" not in data:
            return "Invalid request", 400
        
        name = data["name"]
        price = data["price"]
        
        new_product = Product(name=name, price=price)
        db.session.add(new_product)

        db.session.commit()
        return "Created Successfully", 201
    
# API view - product    
# Update product
@app.route("/api/product/<int:product_id>", methods=["GET", "PUT"])
def api_update_product(product_id):
    product = db.get_or_404(Product, product_id)
 
    if request.method == 'PUT':
        data = request.json
        if "name" not in data:
            return "Invalid request", 400
        
        if "price" < 0 or not isinstance("price", float):
            return "Invalid request", 400
        
        if not isinstance("quantity", int):
            return "Invalid request", 400

        product.name = data['name']
        product.price = data['price']
        product.available =data['quantity']

        db.session.commit()
        return "", 204


# API view - product
# Delete product
@app.route("/api/product/delete/<int:product_id>", methods=['DELETE'] )
def api_delete_product(product_id):
    product = db.get_or_404(Product, product_id)
    db.session.delete(product)
    db.session.commit()
    return "", 204


# list orders
@app.route("/orders", methods=['GET', 'POST'])
def orders_list():
        statement = db.select(Order).order_by(Order.id)
        records = db.session.execute(statement)
        results = records.scalars()
        return render_template("orders.html", orders = results)

# create order
@app.route("/makeorder", methods=['GET', 'POST'])
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

        return redirect(url_for("orders_list"))
  
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

@app.route("/order/<int:order_id>")
def order_details(order_id):
    statement = db.select(ProductOrder).filter_by(order_id=order_id)
    records = db.session.execute(statement)
    results = records.scalars()
    order = db.get_or_404(Order, order_id)
    return render_template("order_details.html", total = order.total, orders = results, order_id = order_id)

@app.route("/order/process/<int:order_id>", methods=["GET","POST"])
def process_order(order_id):
    order= db.get_or_404(Order, order_id)
    strategy = request.form['strategy']
    Order.process(order, strategy)
    db.session.commit()
    return redirect(url_for("orders_list"))
    

@app.route("/order/<int:order_id>/delete", methods=["GET", "POST"])
def order_delete(order_id):
    order = db.get_or_404(Order, order_id)
    if order.processed is not None:
        return redirect(url_for("orders_list"))
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("orders_list"))


# API view
# create Order   
@app.route("/api/orders", methods=["GET", "POST"])
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

# API view    
# delete order
@app.route("/api/order/<int:order_id>/delete", methods=["DELETE"])
def api_delete_order(order_id):
    order = db.get_or_404(Order, order_id)
    db.session.delete(order)
    db.session.commit()
    return "", 204

# API view
# Update order
@app.route("/api/order/<int:order_id>", methods=["GET","PUT"])
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




    

   
    

# show db contents
# @app.route("/customers")
# def customer_list(): 
#     statement = db.select(Customer).order_by(Customer.name)
#     records = db.session.execute(statement)
#     results = records.scalars()
#     return render_template("customers.html", customers = results)

# jsonify
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
