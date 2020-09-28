from backend import db, mongodb
from werkzeug.security import generate_password_hash, check_password_hash


class CurrentDB(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    current_db = db.Column(db.String(50))
    update_to = db.Column(db.String(50))
    is_migrated = db.Column(db.Boolean)

# SQL-Models
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=False)
    surname = db.Column(db.String(50), nullable=False, unique=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    cust = db.relationship('Customer', backref='user')

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name + ' ' + self.surname)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    shopping_cart = db.relationship('Cart', backref='customer')
    street = db.Column(db.String(50))
    house = db.Column(db.Integer)
    zip_code = db.Column(db.Integer)
    city = db.Column(db.String(30))
    country = db.Column(db.String(30))


class CartItem(db.Model):
    """Association class, Cart-Item"""
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    amount = db.Column(db.Integer)
    item = db.relationship('Item')


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    creation_date = db.Column(db.Date)
    items = db.relationship('CartItem', backref='cart')


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Float(2), nullable=False)
    description = db.Column(db.Text())
    amount_available = db.Column(db.Integer, nullable=False)
    build_url = db.Column(db.String(40), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    date = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    delivery_method = db.Column(db.String(50))
    items = db.relationship('OrderItem')


class OrderItem(db.Model):
    """Association class, Order-Item"""
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    amount = db.Column(db.Integer)
    item = db.relationship('Item')

# Mongo-Models
class MongoItem(mongodb.Document):
    id=mongodb.IntField()
    type = mongodb.StringField()
    price = mongodb.FloatField()
    description = mongodb.StringField()
    amount_available = mongodb.IntField()
    build_url = mongodb.StringField()

class MongoCartItem(mongodb.Document):
    amount = mongodb.IntField()
    item = mongodb.DocumentField(MongoItem)

class MongoUser(mongodb.Document):
    id = mongodb.IntField()
    name = mongodb.StringField()
    surname = mongodb.StringField()
    email = mongodb.StringField()
    password = mongodb.StringField()
    cart = mongodb.ListField(mongodb.DocumentField(MongoCartItem))
    orders = mongodb.ListField(mongodb.IntField())

class MongoOrderItem(mongodb.Document):
    amount = mongodb.IntField()
    item = mongodb.DocumentField(MongoItem)

class MongoOrder(mongodb.Document):
    id = mongodb.IntField()
    date = mongodb.DateTimeField()
    status = mongodb.StringField()
    delivery_method = mongodb.StringField()
    items = mongodb.ListField(mongodb.DocumentField(MongoOrderItem))
