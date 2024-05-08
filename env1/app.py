from flask import Flask,render_template,request,jsonify,flash,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
from templates.models import db, Customers,item,cart,sales
import os,io
import base64
import uuid
from flask import send_file
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash,check_password_hash 
from flask_login import LoginManager,login_user,current_user,login_required
from flask import session  # Import session for managing user sessions
from flask_login import current_user  # Import current_user to get the logged-in user
from datetime import datetime  # Import datetime to get the current timestamp


app = Flask(__name__,static_url_path='/static')
app.secret_key = 'Akila178'

 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Akila178@localhost:5432/Grocery"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')


db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Customers.query.get(user_id)

@app.route('/')
def home():
    return render_template('home.html')



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        user = Customers.query.filter_by(email=username).first()
        if user and user.pwd == password:
            login_user(user)  # Log the user in
            return redirect(url_for('getshopping'))  
        else:
            return "Invalid username or password"  # Handle incorrect credentials
    return render_template('login.html')



@app.route('/shopping', methods=['GET', 'POST'])
def getshopping():
    if request.method == 'POST':
        return render_template('shopping.html')  # Return the template
    return render_template('shopping.html')  # Return the template for GET requests as well


@app.route('/signup', methods=['GET','POST'])
def signup():
    """if request.method == 'GET':
        customers = Customers.query.all()
        return jsonify({'Customer details ': [cust.serialize() for cust in customers]})"""

    if request.method == 'POST':
        name = request.form['name']  # Corrected key name
        email=request.form['email']
        pwd=request.form['pwd']
        phone_number = request.form['phone_number']  # Corrected key name
        address = request.form['address']  # Corrected key name
        city=request.form['city']
        state=request.form['state']
        postal_code=request.form['postal_code']
        new_customer = Customers(name=name,email=email,pwd=pwd,phone_number=phone_number,address=address,city=city,state=state,postal_code=postal_code)
        db.session.add(new_customer)
        db.session.commit()
        flash('Signup successful! Please login.') 
        return render_template('login.html') 
    
    return render_template('signup.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
    return render_template('admin.html')

"""def addProduct(itemname, category, qty, price, stock, image_path):
    new_item = item(itemname=itemname, category=category, qty=qty, price=price, stock=stock, image_path=image_path)
    db.session.add(new_item)
    db.session.commit()"""

@app.route('/addProduct',methods=['POST'])
def addProduct():
    if request.method == 'POST':
        itemname = request.form['itemname']  # Corrected key name
        category=request.form['category']
        qty=request.form['qty']
        price=request.form['price']
        stock=request.form['stock']
        image_path = ''
        if 'image' in request.files:
            file = request.files['image']
            # Save the file to a designated folder or process it as needed
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            image_path = file.filename  # Assuming you save the file path
            if file.filename != '':
        # Perform additional checks if needed
                secure_filename = secure_filename(file.filename)
                destination_folder = app.config['UPLOAD_FOLDER']
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                file.save(os.path.join(destination_folder, secure_filename))
                image_path = os.path.join(destination_folder, secure_filename)  # Store the file path

        new_item = item(itemname=itemname,category=category,qty= qty,price=price,stock=stock,image_path=image_path)
        db.session.add(new_item)
        db.session.commit()
    return render_template('admin.html') 





@app.route('/deleteProduct',methods=['POST'])
def deleteProduct():
    if request.method=='POST':
        itemid=request.form['itemid']
        Item = item.query.get(itemid)
        
        if Item:
            db.session.delete(Item)
            db.session.commit()
            return "DELETED SUCCESSFULLY"
    return render_template('admin.html') 

"""@app.route('/images/<string:image_id>')
def serve_image(image_id):
    item = item.query.get(image_id)
    if item and item.image:
        mimetype = None
        if item.image.startswith(b'\xff\xd8\xff\xe0'):
            mimetype = 'image/jpeg'
        elif item.image.startswith(b'\x89\x50\x4e\x47'):
            mimetype = 'image/png'
        elif item.image.startswith(b'\x47\x49\x46\x38'):
            mimetype = 'image/gif'
        if mimetype:
            response = send_file(io.BytesIO(item.image), mimetype=mimetype)
            response.headers['Content-Length'] = len(item.image)
            response.headers['Content-Type'] = mimetype
            return response
    else:
        return 'Image not found', 404"""




@app.route('/shopping/fruits')
def user_fruits():
    # Filter items by category
    fruits_items = item.query.filter_by(category='Fruits').all()
    return render_template('display_items.html', items=fruits_items)

@app.route('/shopping/vegetables')
def user_vegetables():
    # Filter items by category
    veg_items = item.query.filter_by(category='Vegetables').all()
    return render_template('display_items.html', items=veg_items)

@app.route('/shopping/snacks')
def user_snacks():
    # Filter items by category
    snacks_items = item.query.filter_by(category='Snacks').all()
    return render_template('display_items.html', items=snacks_items)


@app.route('/shopping/essentials')
def user_ess():
    # Filter items by category
    ess_items = item.query.filter_by(category='Essentials').all()
    return render_template('display_items.html', items=ess_items)

@app.route('/about')
def about():
    return render_template('about.html') 
from flask_login import current_user

@app.route('/user_profile')
def user_profile():
    user = current_user  # Get the current logged-in user
    return render_template('profile.html', user=user)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if request.method == 'POST':
        itemid = request.form['itemid']
        item_obj = item.query.get(itemid)
        if item_obj:
            # Check if the item is already in the cart
            existing_cart_item = cart.query.filter_by(cusid=current_user.cusid, itemid=itemid).first()
            if existing_cart_item:
                # If the item already exists in the cart, increment the numbers by 1
                existing_cart_item.numbers += 1
            else:
                # If the item doesn't exist in the cart, create a new cart item
                new_cart_item = cart(cusid=current_user.cusid, itemid=itemid,
                                     itemname=item_obj.itemname, category=item_obj.category,
                                     qty=item_obj.qty, price=item_obj.price, stock=item_obj.stock,
                                     image_path=item_obj.image_path, numbers=1)
                db.session.add(new_cart_item)
            
            db.session.commit()
            flash("Item added to cart successfully",'success')
        else:
            print(f"Item with ID {itemid} not found")
            print("Failed to add item to cart.")
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    # Fetch items from the cart for the current user
    cart_item = cart.query.filter_by(cusid=current_user.cusid).all()
    return render_template('cart.html', cart_items=cart_item)

@app.route('/cart/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if request.method == 'POST':
        item_id = request.form['item_id']  # Assuming the item ID is sent in the POST request
        # Retrieve the cart item from the database
        cart_item = cart.query.filter_by(cusid=current_user.cusid, itemid=item_id).first()
        if cart_item:
            if cart_item.numbers > 1:
                # If there is more than one of the item in the cart, decrement the count
                cart_item.numbers -= 1
            else:
                # If there is only one of the item in the cart, remove it completely
                db.session.delete(cart_item)
            db.session.commit()
            # Fetch the updated list of cart items
            updated_cart_items = cart.query.filter_by(cusid=current_user.cusid).all()
            return render_template('cart.html', cart_items=updated_cart_items), 200
        else:
            return 'Item not found in cart', 404
    else:
        return 'Invalid request method', 405


@app.route('/cart/sales', methods=['GET','POST'])
def cart_sales():
    if request.method == 'POST':
        # Get the cart items for the current user
        cart_items = cart.query.filter_by(cusid=current_user.cusid).all()

        # Calculate total amount
        total_amount = sum(item.price * item.numbers for item in cart_items)

        # Generate sales ID (auto-increment)
        latest_sales = sales.query.order_by(sales.salesid.desc()).first()
        salesid = 1 if latest_sales is None else latest_sales.salesid + 1

        # Create a sales record
        new_sale = sales(
            salesid=salesid,
            cusid=current_user.cusid,
            total_amount=total_amount
        )
        db.session.add(new_sale)

        # Commit changes to the database
        db.session.commit()

        # Optionally, clear the cart after checkout
        cart.query.filter_by(cusid=current_user.cusid).delete()
        db.session.commit()

        return jsonify({'message': 'Checkout successful', 'salesid': salesid, 'total_amount': total_amount}), 200
    else:
        return 'Invalid request method', 405

@app.route('/checkout')
def checkout():
    # Fetch items from the cart for the current user
    cart_items = cart.query.filter_by(cusid=current_user.cusid).all()
    
    # Calculate total amount
    total_amount = sum(item.price * item.numbers for item in cart_items)
    
    # Create a new sales record
    new_sale = sales(cusid=current_user.cusid, total_amount=total_amount)
    db.session.add(new_sale)
    db.session.commit()
    
    # Clear the cart for the current user
    cart.query.filter_by(cusid=current_user.cusid).delete()
    db.session.commit()
    
    # Redirect to a thank you page or any other appropriate page
    return render_template('checkout.html', total_amount=total_amount)        



@app.route('/process_payment', methods=['POST'])
def process_payment():
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')

        # Assuming you have logic to generate the bill based on the items in the cart
        total_amount =  request.form.get('total_amount')

        # Here you can include logic to handle different payment methods
        if payment_method == 'credit_card':
            # Handle credit card payment
            return render_template('payment_success.html', total_amount=total_amount, payment_method='Credit Card')
        elif payment_method == 'debit_card':
            # Handle debit card payment
            return render_template('payment_success.html', total_amount=total_amount, payment_method='Debit Card')
        elif payment_method == 'net_banking':
            # Handle net banking payment
            return render_template('payment_success.html', total_amount=total_amount, payment_method='Net Banking')
        elif payment_method == 'cash_on_delivery':
            # Handle cash on delivery
            return render_template('payment_success.html', total_amount=total_amount, payment_method='Cash on Delivery')
        else:
            return "Invalid payment method"

    # If the request method is not POST, redirect to the checkout page
    return redirect(url_for('checkout'))

def calculate_total_amount():
    # Fetch items from the cart for the current user
    cart_items = cart.query.filter_by(cusid=current_user.cusid).all()

    # Calculate total amount by multiplying price and quantity for each item in the cart
    total_amount = sum(item.price * item.numbers for item in cart_items)

    return total_amount

def clear_cart():
    # Remove all items from the cart for the current user
    cart_items = cart.query.filter_by(cusid=current_user.cusid).all()
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)