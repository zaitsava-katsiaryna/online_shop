from abc import ABC, abstractmethod
from backend.models import *
from datetime import datetime, date

class Database(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def add_to_db(self, new_object):
        pass

    @abstractmethod
    def delete_from_db(self, customer_id, cart_item):
        pass

    @abstractmethod
    def check_user(self, email, password):
        pass

    @abstractmethod
    def get_user_by_email(self, email):
        pass

    @abstractmethod
    def create_user(self, name, surname, email, password):
        pass

    @abstractmethod
    def get_all_items(self):
        pass

    @abstractmethod
    def get_cart_by_user_id(self, customer_id):
        pass

    @abstractmethod
    def add_new_cart(self, customer_email):
        pass

    @abstractmethod
    def create_new_order(self, customer_id):
        pass

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_item_by_id(self, item_id):
        pass

    @abstractmethod
    def get_items_of_cart(self, cart):
        pass

    @abstractmethod
    def add_cart_item(self, customer_id, item):
        pass

    @abstractmethod
    def get_full_cart(self, customer_id):
        pass

    @abstractmethod
    def update_cart_item_amount(self, cart_item, new_amount, customer_id):
        pass

    @abstractmethod
    def delete_cart(self, customer_id):
        pass

    @abstractmethod
    def add_cart_items_to_order(self, order, cart):
        pass

    @abstractmethod
    def get_report_info(self):
        pass


class MongoDatabase(Database):
    def __init__(self):
        super().__init__()

    def add_to_db(self, new_object):
        new_object.save()

    def delete_from_db(self, customer_id, cart_item):
        print('Deleting...', cart_item)
        cart_item.remove()
        user = MongoUser.query.filter(MongoUser.id==int(customer_id)).first()
        for item in user.cart:
            if item.item.id == cart_item.item.id:
                user.cart.remove(item)
        user.save()

    def check_user(self, email, password):
        print(MongoUser.query.all())
        user = MongoUser.query.filter(MongoUser.email==email).first()
        if user and user.password == password:
            return user
        return None

    def get_user_by_email(self, email):
        return MongoUser.query.filter(MongoUser.email==email).first()

    def create_user(self, name, surname, email, password):
        users = MongoUser.query.all()
        if users:
            new_id = max([user.id for user in users]) + 1
        else:
            new_id = 1
        return MongoUser(id=new_id, name=name, surname=surname, email=email, password=password, cart=[], orders=[])

    def get_all_items(self):
        return MongoItem.query.all()

    def get_cart_by_user_id(self, customer_id):
        user = MongoUser.query.filter(MongoUser.id==int(customer_id)).first()
        if user:
            return user.cart
        return None

    def add_new_cart(self, customer_id):
        return MongoUser.query.filter(MongoUser.id==int(customer_id)).first()

    def create_new_order(self, customer_id):
        orders = MongoOrder.query.all()
        if orders:
            new_id = max([order.id for order in orders]) + 1
        else:
            new_id = 1
        user = MongoUser.query.filter(MongoUser.id==int(customer_id)).first()
        user.orders.append(new_id)
        user.save()
        return MongoOrder(id=new_id, date=datetime.now(), status='Shipped', delivery_method='Post', items=[])

    def get_all_users(self):
        return MongoUser.query.all()

    def get_item_by_id(self, item_id):
        return MongoItem.query.filter(MongoItem.id==int(item_id)).first()

    def get_items_of_cart(self, cart):
        res = {cart_item.item.id: {'id': cart_item.item.id,
                         'type': cart_item.item.type,
                         'price': cart_item.item.price,
                         'description': cart_item.item.description,
                         'available': cart_item.item.amount_available,
                         'url': cart_item.item.build_url,
                         'amount': cart_item.amount}
               for cart_item in cart}
        return res

    def add_cart_item(self, customer_id, item):
        user = MongoUser.query.filter(MongoUser.id==int(customer_id)).first()
        cart_item = MongoCartItem(amount=1, item=item)
        user.cart.append(cart_item)
        user.save()

    def get_full_cart(self, customer_id):
        pass

    def update_cart_item_amount(self, cart_item, new_amount, customer_id):
        cart_item.amount = new_amount
        cart_item.save()
        user = MongoUser.query.filter(MongoUser.id==int(customer_id)).first()
        for item in user.cart:
            if item.item.id == cart_item.item.id:
                item.amount = new_amount
        user.save()

    def delete_cart(self, customer_id):
        user = MongoUser.query.filter(MongoUser.id==int(customer_id)).first()
        user.cart = []
        user.save()

    def add_cart_items_to_order(self, order, cart):

        for cart_item in cart:
            order_item = MongoOrderItem(amount=cart_item.amount, item=cart_item.item)
            order.items.append(order_item)
            cart_item.remove()
        order.save()

    def get_report_info(self):
        res = []
        users = MongoUser.query.all()
        for user in users:
            for order_id in user.orders:
                order = MongoOrder.query.filter(MongoOrder.id==int(order_id)).first()
                tmp = {
                    'user_id': user.id,
                    'username': user.name + ' ' + user.surname,
                    'order_id': order.id,
                    'order_date': order.date,
                    'order_status': order.status,
                    'items': []
                }
                for order_item in order.items:
                    tmp['items'].append({
                    'item_id': order_item.item.id,
                    'item_type': order_item.item.type,
                    'item_price': order_item.item.price,
                    'amount': order_item.amount
                    })
                res.append(tmp)
        return res


class SQLDatabase(Database):
    def __init__(self):
        super().__init__()

    def add_to_db(self, new_object):
        db.session.add(new_object)
        db.session.commit()

    def delete_from_db(self, customer_id, cart_item):
        db.session.delete(cart_item)
        db.session.commit()

    def check_user(self, email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            return user
        return None

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def create_user(self, name, surname, email, password):
        return User(name=name, surname=surname, email=email, password=password)

    def get_all_items(self):
        return Item.query.all()

    def get_cart_by_user_id(self, customer_id):
        cart = Cart.query.filter_by(customer_id=customer_id).first()
        if cart:
            return cart.items
        return None

    def add_new_cart(self, customer_id):
        cart = Cart(customer_id=customer_id, creation_date=date.today())
        self.add_to_db(cart)
        return cart.items

    def create_new_order(self, customer_id):
        return Order(customer_id=customer_id, date=datetime.now(), status='Shipped', delivery_method='Post')

    def get_all_users(self):
        return User.query.all()

    def get_item_by_id(self, item_id):
        return Item.query.filter_by(id=item_id).first()

    def get_items_of_cart(self, cart):
        res = {cart_item.item_id: {'id': cart_item.item_id,
                         'type': cart_item.item.type,
                         'price': cart_item.item.price,
                         'description': cart_item.item.description,
                         'available': cart_item.item.amount_available,
                         'url': cart_item.item.build_url,
                         'amount': cart_item.amount}
               for cart_item in cart}
        return res

    def get_full_cart(self, customer_id):
        return Cart.query.filter_by(customer_id=customer_id).first()

    def add_cart_item(self, customer_id, item):
        cart = self.get_full_cart(customer_id)
        cart_item = CartItem(amount=1)
        cart_item.item = item
        cart.items.append(cart_item)
        db.session.commit()

    def update_cart_item_amount(self, cart_item, new_amount, customer_id):
        cart_item.amount = new_amount
        db.session.commit()

    def delete_cart(self, customer_id):
        cart = Cart.query.filter_by(customer_id=customer_id).first()
        db.session.delete(cart)
        db.session.commit()

    def add_cart_items_to_order(self, order, cart):
        for cart_item in cart:
            order_item = OrderItem(amount=cart_item.amount)
            order_item.item = cart_item.item
            order.items.append(order_item)
            db.session.delete(cart_item)
        db.session.commit()

    def get_report_info(self):
        joined = db.session.query(User, Order).outerjoin(Order, User.id == Order.customer_id).all()
        res = [{'user_id': j[0].id,
                'username': j[0].name + ' ' + j[0].surname,
                'order_id': j[1].id,
                'order_date': j[1].date,
                'order_status': j[1].status,
                'items': []
                } for j in joined if j[1]]
        for order_item in OrderItem.query.all():
            for r in res:
                if r['order_id'] == order_item.order_id:
                    r['items'].append({'item_id': order_item.item_id,
                                       'item_type': order_item.item.type,
                                       'item_price': order_item.item.price,
                                       'amount': order_item.amount})
        return res
