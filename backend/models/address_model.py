from backend.extensions import db

class Address (db.Model):

    id = db.Column (db.Integer ,primary_key=True)
    user_id = db.Column(db.db.Integer )
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    pincode = db.Column(db.String(20))