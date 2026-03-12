from backend.extensions import db


class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    seller_id = db.Column(db.Integer, db.ForeignKey("seller.id"))

    name = db.Column(db.String(200))

    price = db.Column(db.Float)

    stock = db.Column(db.Integer)

    image = db.Column(db.String(200))