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





if __name__ == '__main__':
    app.run()
