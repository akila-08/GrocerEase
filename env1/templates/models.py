from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy import Sequence

db = SQLAlchemy()


class Customers(db.Model):
    __tablename__ = 'customers'

    cusid = db.Column(db.String(4), primary_key=True, server_default='customer_sequence')
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    pwd = db.Column(db.String(100),nullable=False)
    phone_number = db.Column(db.Numeric(10, 0), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    registration_date = db.Column(db.Date, nullable=False, server_default=db.func.current_date())

    def is_active(self):
        return True
    
    def get_id(self):
        return self.cusid 
    
    def __init__(self,name,email,pwd,phone_number,address,city,state,postal_code):
        self.name = name
        self.email=email
        self.pwd=pwd
        self.phone_number = phone_number
        self.address = address
        self.city=city
        self.state=state
        self.postal_code=postal_code


    def repr(self):
        return f"Cusid: {self.cusid},Name: {self.name}, Email: {self.email}, Pwd:{self.pwd},Phone_number: {self.phone_number}, Address: {self.address}, City: {self.city}, State: {self.state}, Postal_code: {self.postal_code}, Registration_date: {self.registration_date}"
     
    def serialize(self):
        return {
            'cusid': self.cusid,
            'name': self.name,
            'Email':self.email,
            'Pwd':self.pwd,
            'Phone': self.phone_number,
            'Address': self.address,
            'City': self.city,
            'State': self.state,
            'Postal_Code': self.postal_code,
            'Registration_Date': self.registration_date.strftime('%Y-%m-%d') if self.registration_date else None
        }



class item(db.Model):
    __tablename__='item'

    itemid= db.Column(db.String(5), primary_key=True, server_default='ItemIDseq')
    itemname = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    qty=db.Column(db.Numeric(10,0),nullable=False)
    price= db.Column(db.Numeric(5, 2), nullable=False)
    stock=db.Column(db.Numeric(5,0),nullable=False)
    image_path = db.Column(db.String(255),nullable=False)

    __table_args__ = (
        CheckConstraint(func.INITCAP(itemname) == itemname),
        CheckConstraint(category.in_(('Fruits', 'Vegetables', 'Essentials', 'Snacks'))),
        CheckConstraint(qty > 0),
        CheckConstraint(price > 0),
        CheckConstraint(stock >= 0),
    )

    def __init__(self,itemname,category,qty,price,stock,image_path):
        self.itemname = itemname
        self.category=category
        self.qty=qty
        self.price = price
        self.stock = stock
        self.image_path=image_path


    def __repr__(self):
        return f"itemid='{self.itemid}', itemname='{self.itemname}', Category='{self.category}', qty={self.qty}, Price={self.price}, Stock={self.stock},image={self.image_path})"
    
    def serialize(self):
        return {
            'itemid': self.itemid,
            'itemname': self.itemname,
            'category':self.category,
            'qty': self.qty,
            'price':self.price,
            'stock': self.stock,
            'image':self.image_path
        }
   

class cart(db.Model):
    __tablename__ = 'cart'
    cusid = db.Column(db.String(4), db.ForeignKey('customers.cusid'), primary_key=True)
    customer = db.relationship('Customers', backref=db.backref('cart', lazy=True))
    itemid = db.Column(db.String(5), db.ForeignKey('item.itemid'), primary_key=True)
    item = db.relationship('item', backref='carts',lazy=True)
    itemname = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(5, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    numbers = db.Column(db.Integer, nullable=False)

    def __init__(self, cusid, itemid, itemname, category, qty, price, stock, image_path, numbers):
        self.cusid = cusid
        self.itemid = itemid
        self.itemname = itemname
        self.category = category
        self.qty = qty
        self.price = price
        self.stock = stock
        self.image_path = image_path
        self.numbers = numbers

    def __repr__(self):
        return f"cusid='{self.cusid}',itemid={self.itemid}, itemname='{self.itemname}', category='{self.category}', qty={self.qty}, price={self.price}, stock={self.stock}, image={self.image_path}, numbers={self.numbers})"

    def serialize(self):
        return {
            'cusid' : self.cusid,
            'itemid': self.itemid,
            'itemname': self.itemname,
            'category': self.category,
            'qty': self.qty,
            'price': self.price,
            'stock': self.stock,
            'image': self.image_path,
            'numbers': self.numbers
        }
    

class sales(db.Model):
    __tablename__ = 'sales'

    salesid = db.Column(db.Integer, primary_key=True)
    cusid = db.Column(db.String(4), db.ForeignKey('customers.cusid'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    
    customer = db.relationship('Customers', backref='sales')
    def __repr__(self):
        return f"Sales(salesid={self.salesid}, cusid={self.cusid}, total_amount={self.total_amount})"
