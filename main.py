import json
from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import data_file


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lesson_16.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(50))

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


with app.app_context():
    db.drop_all()
    db.create_all()


users = []
for user in data_file.user_data:
    users.append(User(**user))

orders = []
for order in data_file.order_data:
    order['start_date'] = datetime.strptime(order['start_date'], '%m/%d/%Y').date()
    order['end_date'] = datetime.strptime(order['end_date'], '%m/%d/%Y').date()
    orders.append(Order(**order))

offers = []
for offer in data_file.offer_data:
    offers.append(Offer(**offer))

with app.app_context():
    db.session.add_all(users)
    db.session.add_all(orders)
    db.session.add_all(offers)
    db.session.commit()


@app.route('/')
def main_page():
    return 'Главная страница'


@app.route('/users', methods=['GET', 'POST'])
def users_page():
    if request.method == 'GET':
        users = []
        for user in User.query.all():
            users.append(user.to_dict())
        return jsonify(users)
    elif request.method == 'POST':
        user = json.loads(request.data)
        db.session.add(User(**user))
        db.session.commit()
        return 'Пользователь записан'


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_page(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id).to_dict()
        return jsonify(user)
    elif request.method == 'PUT':
        user = json.loads(request.data)
        user_updated = User.query.get(user_id)
        user_updated.first_name = user['first_name']
        user_updated.last_name = user['last_name']
        user_updated.age = user['age']
        user_updated.email = user['email']
        user_updated.role = user['role']
        user_updated.phone = user['phone']
        db.session.add(user_updated)
        db.session.commit()
        return 'Пользователь изменен'
    elif request.method == 'DELETE':
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return 'Пользователь удален'


@app.route('/orders', methods=['GET', 'POST'])
def orders_page():
    if request.method == 'GET':
        orders = []
        for order in Order.query.all():
            orders.append(order.to_dict())
        return jsonify(orders)
    elif request.method == 'POST':
        order = json.loads(request.data)
        order['start_date'] = datetime.strptime(order['start_date'], '%m/%d/%Y').date()
        order['end_date'] = datetime.strptime(order['end_date'], '%m/%d/%Y').date()
        db.session.add(Order(**order))
        db.session.commit()
        return 'Заказ записан'


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def order_page(order_id):
    if request.method == 'GET':
        order = Order.query.get(order_id).to_dict()
        return jsonify(order)
    elif request.method == 'PUT':
        order = json.loads(request.data)
        order_updated = Order.query.get(order_id)
        order_updated.name = order['name']
        order_updated.description = order['description']
        order_updated.start_date = datetime.strptime(order['start_date'], '%m/%d/%Y').date()
        order_updated.end_date = datetime.strptime(order['end_date'], '%m/%d/%Y').date()
        order_updated.address = order['address']
        order_updated.price = order['price']
        order_updated.customer_id = order['customer_id']
        order_updated.executor_id = order['executor_id']
        db.session.add(order_updated)
        db.session.commit()
        return 'Заказ изменен'
    elif request.method == 'DELETE':
        order = Order.query.get(order_id)
        db.session.delete(order)
        db.session.commit()
        return 'Заказ удален'


@app.route('/offers', methods=['GET', 'POST'])
def offers_page():
    if request.method == 'GET':
        offers = []
        for offer in Offer.query.all():
            offers.append(offer.to_dict())
        return jsonify(offers)
    elif request.method == 'POST':
        offer = json.loads(request.data)
        db.session.add(Offer(**offer))
        db.session.commit()
        return 'Предложение записано'


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def offer_page(offer_id):
    if request.method == 'GET':
        offer = Offer.query.get(offer_id).to_dict()
        return jsonify(offer)
    elif request.method == 'PUT':
        offer = json.loads(request.data)
        offer_updated = Offer.query.get(offer_id)
        offer_updated.order_id = offer['order_id']
        offer_updated.executor_id = offer['executor_id']
        db.session.add(offer_updated)
        db.session.commit()
        return 'Запрос изменен'
    elif request.method == 'DELETE':
        offer = Offer.query.get(offer_id)
        db.session.delete(offer)
        db.session.commit()
        return 'Запрос удален'


if __name__ == '__main__':
    app.run()
