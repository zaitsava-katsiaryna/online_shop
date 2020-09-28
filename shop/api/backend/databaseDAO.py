
from backend.db_init import get_database

def check_user(email, password):
    database = get_database()
    if not database:
        return None
    return database.check_user(email, password)


def get_user_by_email(email):
    database = get_database()
    if not database:
        return None
    return database.get_user_by_email(email)

def add_new_user(name, surname, email, password):
    database = get_database()
    if not database:
        return False
    if database.get_user_by_email(email):
        return False
    new_user = database.create_user(name, surname, email, password)

    database.add_to_db(new_user)
    return True

def get_all_items():
    database = get_database()
    if not database:
        return None
    res = {item.id: {'id': item.id,
                     'type': item.type,
                     'price': item.price,
                     'description': item.description,
                     'available': item.amount_available,
                     'url': item.build_url}
           for item in database.get_all_items()}
    return res

def get_cart_by_user_id(customer_id):
    database = get_database()
    if not database:
        return None
    return database.get_cart_by_user_id(customer_id)

def add_new_cart(customer_id):
    database = get_database()
    if not database:
        return None
    new_cart = database.add_new_cart(customer_id)
    return new_cart

def get_item_by_id(item_id):
    database = get_database()
    if not database:
        return None
    return database.get_item_by_id(item_id)

def get_items_of_cart(cart):
    database = get_database()
    if not database:
        return None
    return database.get_items_of_cart(cart)

def get_report_info():
    database = get_database()
    if not database:
        return None
    return database.get_report_info()

def add_new_order(customer_id):
    database = get_database()
    if not database:
        return None
    new_order = database.create_new_order(customer_id)
    database.add_to_db(new_order)
    return new_order

def add_new_cart_item(customer_id, item):
    database = get_database()
    if not database:
        return
    database.add_cart_item(customer_id, item)

def update_cart_item_amount(cart_item, new_amount, customer_id):
    database = get_database()
    if not database:
        return
    database.update_cart_item_amount(cart_item, new_amount, customer_id)

def delete_from_db(customer_id, cart_item):
    database = get_database()
    if not database:
        return
    database.delete_from_db(customer_id, cart_item)

def delete_cart(customer_id):
    database = get_database()
    if not database:
        return
    database.delete_cart(customer_id)

def add_cart_items_to_order(order, cart):
    database = get_database()
    if not database:
        return
    database.add_cart_items_to_order(order, cart)
