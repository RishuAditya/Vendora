from flask import Blueprint, render_template
from flask_login import login_required, current_user

from backend.models.user_model import User
from backend.models.product_model import Product
from backend.models.order_model import Order
from backend.models.seller_model import Seller

admin_bp = Blueprint("admin", __name__)


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