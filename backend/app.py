import os
from flask import Flask, render_template
from flask_login import login_required, current_user

from backend.extensions import db, login_manager
from backend.routes.auth_routes import auth_bp
from backend.routes.product_routes import product_bp
from backend.models.order_model import Order
from backend.routes.order_routes import order_bp
from backend.models.user_model import User
from backend.models.seller_model import Seller
from backend.models.product_model import Product
from backend.models.cart_model import Cart
from backend.routes.cart_routes import cart_bp

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, "../frontend/templates"),
    static_folder=os.path.join(base_dir, "../frontend/static"),
)

# Config
app.config["SECRET_KEY"] = "mysecret"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Rishu1309@localhost/vendora"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- DASHBOARDS ----------------
@app.route("/admin")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        return "Access Denied"
    return f"Admin Dashboard - Welcome {current_user.name}"


@app.route("/seller")
@login_required
def seller_dashboard():
    if current_user.role != "seller":
        return "Access Denied"
    return f"Seller Dashboard - Welcome {current_user.name}"


@app.route("/customer")
@login_required
def customer_dashboard():
    if current_user.role != "customer":
        return "Access Denied"
    return f"Customer Dashboard - Welcome {current_user.name}"

# ---------------- USER LOADER ----------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


login_manager.init_app(app)

# create tables
with app.app_context():
    db.create_all()