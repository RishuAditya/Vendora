from flask import Blueprint, render_template
from flask_login import login_required, current_user

from backend.models.product_model import Product
from backend.models.order_model import Order
from backend.models.seller_model import Seller

seller_bp = Blueprint("seller", __name__)


# -------- SELLER DASHBOARD --------
@seller_bp.route("/seller/dashboard")
@login_required
def seller_dashboard():

    if current_user.role != "seller":
        return "Access Denied"

    seller = Seller.query.filter_by(user_id=current_user.id).first()

    if not seller:
        return "Seller profile not found"

    # Seller Products
    products = Product.query.filter_by(seller_id=seller.id).all()
    total_products = len(products)

    product_ids = [p.id for p in products]

    # Seller Orders
    orders = Order.query.filter(Order.product_id.in_(product_ids)).all()
    total_orders = len(orders)

    # Revenue Calculation
    total_revenue = 0

    for order in orders:
        product = Product.query.get(order.product_id)

        if product:
            total_revenue += product.price * order.quantity

    # -------- BEST SELLING PRODUCT --------
    best_product = None
    best_sales = 0

    for product in products:
        sales = Order.query.filter_by(product_id=product.id).count()

        if sales > best_sales:
            best_sales = sales
            best_product = product.name

    # -------- LOW STOCK ALERT --------
    low_stock = []

    for product in products:
        if product.stock < 5:
            low_stock.append(product)

    return render_template(
        "seller/dashboard.html",
        total_products=total_products,
        total_orders=total_orders,
        total_revenue=total_revenue,
        best_product=best_product,
        low_stock=low_stock
    )