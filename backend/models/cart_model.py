from backend.extensions import db

class Cart(db.Model):

    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))

    quantity = db.Column(db.Integer, default=1)