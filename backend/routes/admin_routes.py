from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from backend.extensions import db
from backend.models.user_model import User
from backend.models.product_model import Product
from backend.models.order_model import Order
from backend.models.seller_model import Seller

admin_bp = Blueprint("admin", __name__)


# ---------------- ADMIN DASHBOARD ----------------

@admin_bp.route("/admin/dashboard")
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        return "Access Denied"

    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_sellers = Seller.query.count()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_products=total_products,
        total_orders=total_orders,
        total_sellers=total_sellers
    )


# ---------------- VIEW ALL PRODUCTS ----------------

@admin_bp.route("/admin/products")
@login_required
def admin_products():

    if current_user.role != "admin":
        return "Access Denied"

    products = Product.query.all()

    return render_template(
        "admin/products.html",
        products=products
    )


# ---------------- DELETE PRODUCT ----------------

@admin_bp.route("/admin/delete-product/<int:id>")
@login_required
def delete_product(id):

    if current_user.role != "admin":
        return "Access Denied"

    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return redirect("/admin/products")


# ---------------- VIEW USERS ----------------

@admin_bp.route("/admin/users")
@login_required
def admin_users():

    if current_user.role != "admin":
        return "Access Denied"

    users = User.query.all()

    return render_template(
        "admin/users.html",
        users=users
    )


# ---------------- BAN USER ----------------

@admin_bp.route("/admin/ban-user/<int:id>")
@login_required
def ban_user(id):

    if current_user.role != "admin":
        return "Access Denied"

    user = User.query.get(id)

    user.status = "banned"

    db.session.commit()

    return redirect("/admin/users")