from backend.extensions import db
from backend.models.seller_model import Seller
from backend.models.category_model import Category

class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"))

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)

    image = db.Column(db.String(200))

    category = db.relationship("Category")