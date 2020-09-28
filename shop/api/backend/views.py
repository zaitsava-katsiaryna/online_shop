from backend import app
from backend.models import *
from backend.db_init import init_db, toggle_database, drop_all, get_current_database
from flask import jsonify, request
from .models import db, User
from flask_jwt_extended import create_access_token
from datetime import datetime, date
from backend.databaseDAO import *


@app.route('/drop')
def drop_table():
    drop_all()
    return 'Dropped'

@app.route('/fill')
def fill_db():
    init_db()
    return 'Filled'

@app.route('/current')
def get_current_db():
    curr = get_current_database()
    return jsonify(current_db=curr)

@app.route('/toggle')
def toggling_database():
    update_to = toggle_database()
    curr = get_current_database()
    return jsonify(update_to=update_to, current_db=curr)

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": 'Missing json in request'}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = check_user(email, password)

    if not user:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify(access_token=access_token, user_id=user.id, username=user.name + ' ' + user.surname), 200


@app.route('/signup', methods=['POST'])
def signup():
    if not request.is_json:
        return jsonify({'msg': 'Missing json in request'}), 400

    name = request.json.get('name', None)
    surname = request.json.get('surname', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    is_added = add_new_user(name, surname, email, password)
    if not is_added:
        return jsonify({'msg': 'User with email ' + email + ' is already registered'}), 500
        print('hello')
    return 'Signed up!'

@app.route('/items', methods=['GET'])
def get_items():
    items = get_all_items()
    return jsonify(items)


@app.route('/cart_items/<int:customer_id>', methods=['GET'])
def get_cart_items(customer_id):
    """Get cart items given user id. If no cart is provided - create one"""
    cart = get_cart_by_user_id(customer_id)
    print('Cart: ', cart)
    if cart:
        res = get_items_of_cart(cart)
        print('Cart items: ', res)
        return jsonify(res)
    add_new_cart(customer_id)
    return {}


@app.route('/item/<item_id>')
def get_item(item_id):
    item = get_item_by_id(item_id)
    if not item:
        return jsonify({"msg": "Item not found"}), 404

    to_return = {'id': item.id, 'type': item.type, 'price': item.price, 'description': item.description,
                        'available': item.amount_available, 'url': item.build_url}
    return jsonify(to_return)


@app.route('/report')
def generate_report():
    res = get_report_info()
    return jsonify(res)


@app.route('/checkout/<customer_id>')
def checkout(customer_id):

    cart = get_cart_by_user_id(customer_id)

    if cart:
        order = add_new_order(customer_id)
        add_cart_items_to_order(order, cart)
        delete_cart(customer_id)

        return 'Checked out successfully'
    return 'Cart is empty'


@app.route('/add_cart_item/<customer_id>/<int:item_id>')
def add_cart_item(customer_id, item_id):
    item = get_item_by_id(item_id)
    cart = get_cart_by_user_id(customer_id)
    if cart == None:
        cart = add_new_cart(customer_id)

    for cart_item in cart:
        if cart_item.item.id == item_id:
            return jsonify('Error: item is already in the cart'), 500

    add_new_cart_item(customer_id, item)

    return jsonify('Success! Item added to cart :)')


@app.route('/update_cart_item/<int:customer_id>/<int:item_id>/<int:new_amount>', methods=['PUT'])
def update_amount(customer_id, item_id, new_amount):
    cart = get_cart_by_user_id(customer_id)
    for cart_item in cart:
        if cart_item.item.id == item_id:
            update_cart_item_amount(cart_item, new_amount, customer_id)

    return 'Success :)'


@app.route('/remove_cart_item/<int:customer_id>/<int:item_id>', methods=['DELETE'])
def remove_item(customer_id, item_id):
    cart = get_cart_by_user_id(customer_id)

    for cart_item in cart:  # search for item with given id in the cart
        if cart_item.item.id == item_id:  # if found - delete item
            delete_from_db(customer_id, cart_item)

    return jsonify('Done with removing')
