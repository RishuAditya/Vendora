from backend.extensions import db

class Wishlist(db.Model):

    __tablename__ = "wishlist"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))