from backend.models import CurrentDB, User, Item, Customer, Order, OrderItem, Cart, MongoItem, MongoUser, MongoOrder, MongoCartItem, MongoOrderItem
from random import randint, uniform
import secrets
from backend import db, mongodb
from datetime import datetime
from backend.Database import MongoDatabase, SQLDatabase


def get_current_database():
    database = get_database()
    if isinstance(database, SQLDatabase):
        return 'SQL'
    elif isinstance(database, MongoDatabase):
        return 'Mongo'
    return 'None'

def get_database():
    curr_db = CurrentDB.query.filter_by(id=1).first()
    print('Current db: ', curr_db)
    if not curr_db:
        curr_db = update_database()
    if curr_db.current_db == 'Mongo':
        return MongoDatabase()
    elif curr_db.current_db == 'SQL':
        return SQLDatabase()
    print('Curr db now:', curr_db)
    return None

def update_database():
    curr_db = CurrentDB.query.filter_by(id=1).first()
    if not curr_db:
        curr_db = CurrentDB(current_db='SQL', update_to='Mongo', is_migrated=False)
        db.session.add(curr_db)
        db.session.commit()
        return curr_db
    if curr_db.current_db == 'Mongo':
        curr_db.current_db = 'SQL'
        curr_db.update_to = 'Mongo'
    elif curr_db.current_db == 'SQL':
        curr_db.current_db = 'Mongo'
        curr_db.update_to = 'SQL'
        if not curr_db.is_migrated:
            migrate()
            curr_db.is_migrated = True
    print(curr_db.current_db, curr_db.update_to, curr_db.is_migrated)
    db.session.commit()
    return curr_db

def toggle_database():
    """Switch database"""
    database = get_database()
    print('Switching...')
    if database:
        print('Database exist!')
        update_database()
    else:
        print('Something went wrong')

    return 'Hop hey'

def migrate():
    sql_users = User.query.all()
    sql_carts = Cart.query.all()
    sql_items = Item.query.all()
    sql_orders = Order.query.all()

    for item in MongoItem.query.all():
        item.remove()

    for user in MongoUser.query.all():
        user.remove()

    for order in MongoOrder.query.all():
        order.remove()

    for item in sql_items:
        mongo_item = MongoItem(
        id=item.id,
        type=item.type,
        price=item.price,
        description=item.description,
        amount_available=item.amount_available,
        build_url=item.build_url
        )
        mongo_item.save()

    for user in sql_users:
        user_cart = Cart.query.filter_by(customer_id=user.id).first()
        user_orders = list(Order.query.filter_by(customer_id=user.id))
        mongo_user = MongoUser(
        id=user.id,
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=user.password,
        cart = [],
        orders = []
        )
        if user_cart:
            for cart_item in user_cart.items:
                mongo_item = MongoItem.query.filter(MongoItem.id==cart_item.item_id).first()
                mongo_cart_item = MongoCartItem(amount=cart_item.amount, item=mongo_item)
                mongo_user.cart.append(mongo_cart_item)
        if user_orders:
            for order in user_orders:
                for order_item in order.items:
                    mongo_item = MongoItem.query.filter(MongoItem.id==order_item.item_id).first()
                    mongo_order_item = MongoCartItem(amount=order_item.amount, item=mongo_item)
                    mongo_order_item.save()
                mongo_user.orders.append(order.id)
            print(mongo_user.name, mongo_user.orders)
        mongo_user.save()

    for order in sql_orders:

        mongo_order = MongoOrder(
        id=order.id,
        date = order.date,
        status = order.status,
        delivery_method = order.delivery_method,
        items = []
        )

        for item in order.items:
            mongo_item = MongoItem.query.filter(MongoItem.id == item.item_id).first()
            mongo_order_item = MongoOrderItem(amount=item.amount, item=mongo_item)
            mongo_order.items.append(mongo_order_item)
        mongo_order.save()

def drop_all():
    db.drop_all()
    db.create_all()


def init_db():
    db.create_all()
    print('INIT DB!!!!')
    curr_db = CurrentDB.query.filter_by(id=1).first()
    if not curr_db:
        curr_db = CurrentDB(current_db='SQL', update_to='Mongo', is_migrated=False)
        print('Current db: ', curr_db.current_db, curr_db.update_to, curr_db.is_migrated)
        db.session.add(curr_db)
        db.session.commit()



    mails = ['@gmail.com', '@yahoo.com', '@univie.ac.at', '@mail.com', '@outlook.com']

    first_names = ['Lee', 'Kye', 'Penelope', 'Demi', 'Flora', 'Alexia', 'Amelia', 'Claudia', 'Lachlan', 'Esme',
                   'Annabel',
                   'Charley', 'Evangeline', 'Milly', 'Paige', 'Sam', 'Yasmin', 'Minnie', 'Annabelle', 'Abigail', 'Ray',
                   'Lisa', 'Stacey', 'Jenna', 'Courtney', 'Ronnie', 'Troy', 'Ana']

    last_names = ['Anderson', 'Barton', 'Norris', 'Johnson', 'Newman', 'Hart', 'Wong', 'Woods', 'Houston', 'Armstrong',
                  'Yang', 'Rose', 'Cole', 'Harper', 'Owens', 'Webb', 'Nelson', 'Drake', 'Patton', 'Smart', 'Hansen',
                  'Poole', 'Parsons', 'Moran', 'Rees', 'Stokes', 'Simpson', 'Klein', 'Schneider', 'Henderson', 'Cross',
                  'Kelly', 'Vega']

    types = ['Earrings', 'Necklace', 'Bracelet']

    build_urls = ['https://picsum.photos/600/300/?image=25']


    # add random users
    for _ in range(10):
        name = first_names[randint(0, len(first_names) - 1)]
        surname = last_names[randint(0, len(last_names) - 1)]
        email = name.lower() + '.' + surname.lower() + str(randint(1, 50) * randint(51, 100)) + mails[
            randint(0, len(mails) - 1)]
        password = secrets.token_urlsafe(20)
        user = User(name=name, surname=surname, email=email, password=password)

        db.session.add(user)

        inserted_user = User.query.filter_by(email=email).first()

        customer = Customer(user_id=inserted_user.id, house=randint(1, 10))
        db.session.add(customer)

    test_user = User(name='test', surname='test', email='test@mail.com', password='test')
    db.session.add(test_user)
    inserted_test = User.query.filter_by(email='test@mail.com').first()
    customer = Customer(user_id=inserted_test.id, house=randint(1, 10))
    db.session.add(customer)
    db.session.commit()

    res = db.session.query(User, Customer).outerjoin(Customer, User.id == Customer.user_id).all()

    local_items = []
    # add random items
    for _ in range(15):
        type = types[randint(0, len(types) - 1)]
        url = build_urls[randint(0, len(build_urls) - 1)]
        price = round(uniform(5, 50), 2)
        description = 'Best wooden jewellery item ever, I tell you! '
        amount_available = randint(0, 10)

        # print(type, price, description, amount_available, url)
        item = Item(type=type, price=price, description=description, amount_available=amount_available, build_url=url)
        local_items.append(item)
        db.session.add(item)

    db.session.commit()

    # add orders to couple of users

    for i in range(7):
        customer_id = i+1

        order = Order(customer_id=customer_id, date=datetime.now(), status='Shipped', delivery_method='Post')

        db.session.add(order)
        db.session.commit()

        for j in range(randint(1, 2)):
            order_item = OrderItem(amount=randint(1, 5))
            if j % 2 == 0:
                item = local_items[randint(0, int(len(local_items) / 2))]
            else:
                item = local_items[randint(int(len(local_items) / 2), len(local_items)-1)]
            order_item.item = item
            order.items.append(order_item)

            db.session.commit()
    print(Item.query.all())
