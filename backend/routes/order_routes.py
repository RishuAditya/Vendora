from flask import Blueprint, redirect, render_template
from flask_login import login_required, current_user

from backend.extensions import db
from backend.models.cart_model import Cart
from backend.models.order_model import Order

order_bp = Blueprint("order", __name__)


# ---------------- CHECKOUT ----------------
@order_bp.route("/checkout")
@login_required
def checkout():

    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    for item in cart_items:

        order = Order(
            user_id=current_user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )

        db.session.add(order)

    Cart.query.filter_by(user_id=current_user.id).delete()

    db.session.commit()

    return redirect("/orders")

# -----  Oders view pages..
from flask import render_template
from flask_login import login_required, current_user
from backend.models.order_model import Order
from backend.models.product_model import Product

@order_bp.route("/orders")
@login_required
def my_orders():

    orders = Order.query.filter_by(user_id=current_user.id).all()

    order_data = []

    for order in orders:

        product = Product.query.get(order.product_id)

        if product:
            order_data.append({
                "product_name": product.name,
                "price": product.price,
                "quantity": order.quantity,
                "status": order.status
            })

    return render_template("customer/orders.html", orders=order_data)

# --- Seller order

@order_bp.route("/seller/orders")
@login_required
def seller_orders():

    from backend.models.product_model import Product
    from backend.models.seller_model import Seller

    seller = Seller.query.filter_by(user_id=current_user.id).first()

    if not seller:
        return "Seller not found"

    products = Product.query.filter_by(seller_id=seller.id).all()

    orders_data = []

    for product in products:

        product_orders = Order.query.filter_by(product_id=product.id).all()

        for order in product_orders:
                orders_data.append({
                "id": order.id,
                "product": product.name,
                "quantity": order.quantity,
                "status": order.status
            })

    return render_template("seller/orders.html", orders=orders_data)

#---- Order Status ----------------------

@order_bp.route("/seller/update-order/<int:order_id>/<status>")
@login_required
def update_order(order_id, status):

    order = Order.query.get(order_id)

    if not order:
        return "Order not found"

    order.status = status

    db.session.commit()

    return redirect("/seller/orders")

# -- My oder

