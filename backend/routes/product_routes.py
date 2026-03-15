import os
from flask import Blueprint, current_app, render_template, request, redirect
from flask_login import login_required, current_user
from flask import request, jsonify

from backend.extensions import db
from backend.models.product_model import Product
from backend.models.category_model import Category
from backend.models.seller_model import Seller
from werkzeug.utils import secure_filename


product_bp = Blueprint("product", __name__)


# ---------------- ADD PRODUCT ----------------
@product_bp.route("/seller/add-product", methods=["GET", "POST"])
@login_required
def add_product():

    if current_user.role != "seller":
        return "Access Denied"

    seller = Seller.query.filter_by(user_id=current_user.id).first()

    if not seller:
        seller = Seller(user_id=current_user.id, company_name="My Store")
        db.session.add(seller)
        db.session.commit()

    # ---- FETCH CATEGORIES ----
    categories = Category.query.all()

    if request.method == "POST":

        name = request.form["name"]
        price = request.form["price"]
        stock = request.form["stock"]
        image = request.form.get("image")

        description = request.form.get("description")
        specifications = request.form.get("specifications")
        category_id = request.form.get("category_id")

        # -------- IMAGE UPLOAD --------
        image_file = request.files["image"]

        filename = secure_filename(image_file.filename)

        upload_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], filename
        )

        image_file.save(upload_path)

        # -------- SAVE PRODUCT --------
        product = Product(
            seller_id=seller.id,
            name=name,
            price=price,
            stock=stock,
            image=filename,
            description=description,
            specifications=specifications,
            category_id=category_id
        )

        db.session.add(product)
        db.session.commit()

        return redirect("/seller/products")

    return render_template(
        "seller/add_product.html",
        categories=categories
    )


# ---------------- SELLER PRODUCT LIST ----------------
@product_bp.route("/seller/products")
@login_required
def seller_products():

    seller = Seller.query.filter_by(user_id=current_user.id).first()

    if not seller:
        return "No seller profile found"

    products = Product.query.filter_by(seller_id=seller.id).all()

    return render_template("seller/manage_products.html", products=products)


# ---------------- MARKETPLACE + SEARCH + FILTER + REVIEW ----------------
@product_bp.route("/products")
def products():

    search = request.args.get("search")
    category_id = request.args.get("category")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")

    query = Product.query

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if min_price:
        query = query.filter(Product.price >= min_price)

    if max_price:
        query = query.filter(Product.price <= max_price)

    products = query.all()

    from backend.models.review_model import Review
    reviews = Review.query.all()

    categories = Category.query.all()

    return render_template(
        "customer/products.html",
        products=products,
        reviews=reviews,
        categories=categories
    )


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


# ---------------- ADD TO WISHLIST ----------------
@product_bp.route("/add-to-wishlist/<int:product_id>")
@login_required
def add_to_wishlist(product_id):

    from backend.models.wishlist_model import Wishlist

    item = Wishlist(
        user_id=current_user.id,
        product_id=product_id
    )

    db.session.add(item)
    db.session.commit()

    return redirect("/products")


# ---------------- VIEW WISHLIST ----------------
@product_bp.route("/wishlist")
@login_required
def view_wishlist():

    from backend.models.wishlist_model import Wishlist

    items = Wishlist.query.filter_by(user_id=current_user.id).all()

    products = []

    for item in items:
        product = Product.query.get(item.product_id)
        products.append(product)

    return render_template("customer/wishlist.html", products=products)


# ---------------- REMOVE FROM WISHLIST ----------------
@product_bp.route("/remove-from-wishlist/<int:product_id>")
@login_required
def remove_from_wishlist(product_id):

    from backend.models.wishlist_model import Wishlist

    item = Wishlist.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if item:
        db.session.delete(item)
        db.session.commit()

    return redirect("/wishlist")


# ---------------- ADD REVIEW ----------------
@product_bp.route("/add-review/<int:product_id>", methods=["POST"])
@login_required
def add_review(product_id):

    from backend.models.review_model import Review

    rating = request.form["rating"]
    comment = request.form["comment"]

    review = Review(
        user_id=current_user.id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )

    db.session.add(review)
    db.session.commit()

    return redirect("/products")

# -- Product Detail Route ----

@product_bp.route("/product/<int:product_id>")
def product_detail(product_id):

    product = Product.query.get(product_id)

    return render_template(
        "customer/product_detail.html",
        product=product
    )
# --- REcent product ---
@product_bp.route("/recent-products")
def recent_products():

    ids = request.args.get("ids")

    if not ids:
        return jsonify([])

    ids_list = ids.split(",")

    products = Product.query.filter(Product.id.in_(ids_list)).all()

    data = []

    for p in products:
        data.append({
            "id": p.id,
            "name": p.name,
            "price": p.price
        })

    return jsonify(data)

#-- Trend
@product_bp.route("/trending-products")
def trending_products():

    products = Product.query.order_by(Product.views.desc()).limit(5).all()

    return render_template(
        "customer/trending.html",
        products=products
    )