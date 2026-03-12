from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

from backend.extensions import db
from backend.models.product_model import Product
from backend.models.seller_model import Seller

product_bp = Blueprint("product", __name__)


# ---------------- ADD PRODUCT ----------------
@product_bp.route("/seller/add-product", methods=["GET", "POST"])
@login_required
def add_product():

    if current_user.role != "seller":
        return "Access Denied"

    seller = Seller.query.filter_by(user_id=current_user.id).first()

    # अगर seller record नहीं है तो बना दो
    if not seller:
        seller = Seller(user_id=current_user.id, company_name="My Store")
        db.session.add(seller)
        db.session.commit()

    if request.method == "POST":

        name = request.form["name"]
        price = request.form["price"]
        stock = request.form["stock"]
        image = request.form["image"]

        product = Product(
            seller_id=seller.id,
            name=name,
            price=price,
            stock=stock,
            image=image
        )

        db.session.add(product)
        db.session.commit()

        return redirect("/seller/products")

    return render_template("seller/add_product.html")


# ---------------- SELLER PRODUCT LIST ----------------
@product_bp.route("/seller/products")
@login_required
def seller_products():

    seller = Seller.query.filter_by(user_id=current_user.id).first()

    if not seller:
        return "No seller profile found"

    products = Product.query.filter_by(seller_id=seller.id).all()

    return render_template("seller/manage_products.html", products=products)


# ---------------- CUSTOMER PRODUCT VIEW ----------------
@product_bp.route("/products")
def view_products():

    products = Product.query.all()

    return render_template("customer/products.html", products=products)

# ---------------- ADD TO CART ----------------
@product_bp.route("/add-to-cart/<int:product_id>")
@login_required
def add_to_cart(product_id):

    from backend.models.cart_model import Cart

    cart_item = Cart(
        user_id=current_user.id,
        product_id=product_id,
        quantity=1
    )

    db.session.add(cart_item)
    db.session.commit()

    return redirect("/products")