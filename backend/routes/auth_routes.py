
from flask import Blueprint, render_template, request, redirect,flash

from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


import uuid
from backend.extensions import db
from backend.models.user_model import User
from backend.models.seller_model import Seller
from backend.utils.role_required import role_required
from backend.extensions import db

auth_bp = Blueprint("auth", __name__)


# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form.get("role")

        hashed_password = generate_password_hash(password)

        user = User(
            name=name,
            email=email,
            password=hashed_password,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        if role == "seller":
            seller = Seller(user_id=user.id, company_name="My Store")
            db.session.add(seller)
            db.session.commit()

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            if user.role == "admin":
                return redirect("/admin")

            elif user.role == "seller":
                return redirect("/seller")

            else:
                return redirect("/customer")

        else:
            return "Invalid Email or Password"

    return render_template("login.html")

    print("Entered password:", password)
    print("DB password:", user.password)

# ---------------- LOGOUT ----------------
@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()
    return redirect("/")


# -   Forgot Password ---- 

@auth_bp.route("/forgot-password", methods=["GET","POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form.get("email")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not found")
            return redirect("/forgot-password")

        token = str(uuid.uuid4())

        user.reset_token = token
        db.session.commit()

        reset_link = f"http://127.0.0.1:5000/reset-password/{token}"

        print("Reset link:", reset_link)

        flash("Password reset link generated (check console)")

    return render_template("auth/forgot_password.html")


# ---- reset pasword --

@auth_bp.route("/reset-password/<token>", methods=["GET","POST"])
def reset_password(token):

    user = User.query.filter_by(reset_token=token).first()

    if not user:
        return "Invalid or expired token"

    if request.method == "POST":

        new_password = request.form.get("password")

        user.password = generate_password_hash(new_password)
        user.reset_token = None

        db.session.commit()

        return redirect("/login")

    return render_template("auth/reset_password.html")