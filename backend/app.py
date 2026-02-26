import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from backend.extensions import db, login_manager
from backend.models.user_model import User

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, '../frontend/templates'),
    static_folder=os.path.join(base_dir, '../frontend/static')
)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mysecret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Rishu1309@localhost/vendora'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))
        role = request.form.get('role')

        user = User(name=name, email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for('login'))

    return render_template('register.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            # Role-based redirect
            if user.role == "admin":
                return redirect(url_for('admin_dashboard'))
            elif user.role == "seller":
                return redirect(url_for('seller_dashboard'))
            else:
                return redirect(url_for('customer_dashboard'))

        flash("Invalid credentials")

    return render_template('login.html')


# ---------------- DASHBOARDS ----------------
@app.route('/admin')
@login_required
def admin_dashboard():
    return f"Admin Dashboard - Welcome {current_user.name}"


@app.route('/seller')
@login_required
def seller_dashboard():
    return f"Seller Dashboard - Welcome {current_user.name}"


@app.route('/customer')
@login_required
def customer_dashboard():
    return f"Customer Dashboard - Welcome {current_user.name}"


# ---------------- LOGOUT ----------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ---------------- USER LOADER ----------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    app.run(debug=True)