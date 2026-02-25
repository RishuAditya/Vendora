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

# Import models AFTER db initialization
from backend.models.user_model import User


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))

        flash("Invalid credentials")

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # return f"Welcome {current_user.name}! Role: {current_user.role}"
    return render_template("dashboard.html")
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    app.run(debug=True)