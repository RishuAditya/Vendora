from backend.extensions import db

class Review(db.Model):

    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))

    rating = db.Column(db.Integer)

    comment = db.Column(db.Text)