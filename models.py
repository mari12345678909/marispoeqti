from flask_login import UserMixin

from extension import db, app, login_manager



class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def save(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(60), default='Guest')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Product (db.Model,BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    img = db.Column(db.String)


if __name__ == "__main__":
    products = [
        {"name": "წითელი ვარდების თაიგული 14 ვარდით", "price": 50, "id": 0,
         "img": "https://orqidea.ge/uploads/images/orqidea_1629746952.jpg"},
        {"name": "ვარდისფერი ვარდების თაიგული 30 ვარდით", "price": 50, "id": 1,
         "img": "https://d2j6dbq0eux0bg.cloudfront.net/images/83115755/3530547708.webp"},
        {"name": "საშუალო ზომის იასამნის და ტიტების თაიგული", "price": 50, "id": 2,
         "img": "https://orqidea.ge/uploads/images/orqidea_1682968387.jpg"},
        {"name": "ვარდიფერი ტიტების თაიგული 15 ტიტით", "price": 50, "id": 3, "img": ""},
        {"name": "დიდი თეთრი ვერდების თაიგული 150 გრძელი თეთრი ვარდით", "price": 50, "id": 4, "img": ""},
        {"name": "გვირილების თაიგული 30 გვირილით", "price": 50, "id": 5, "img": ""},
    ]

    with app.app_context():
        db.create_all()

        for product in products:
            new_product = Product(name=product["name"], price=product["price"], img=product["img"])
            new_product.create()
