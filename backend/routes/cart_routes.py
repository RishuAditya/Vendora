from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from backend.extensions import db
from backend.models.cart_model import Cart
from backend.models.product_model import Product

cart_bp = Blueprint("cart", __name__)


# ---------------- VIEW CART ----------------
@cart_bp.route("/cart")
@login_required
def view_cart():

    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    products = []
    total = 0

    for item in cart_items:

        product = Product.query.get(item.product_id)

        if product:
            products.append({
                "cart_id": item.id,
                "name": product.name,
                "price": product.price,
                "quantity": item.quantity
            })

            total += product.price * item.quantity

    return render_template("customer/cart.html", products=products, total=total)


# ---------------- REMOVE CART ITEM ----------------
@cart_bp.route("/remove-cart/<int:id>")
@login_required
def remove_cart(id):

    item = Cart.query.get(id)

    if item:
        db.session.delete(item)
        db.session.commit()

    return redirect("/cart")