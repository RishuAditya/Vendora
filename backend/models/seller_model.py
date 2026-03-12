from backend.extensions import db

class Seller(db.Model):

    __tablename__ = "seller"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    company_name = db.Column(db.String(200))