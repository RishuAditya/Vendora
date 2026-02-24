from flask import Flask, render_template
import os

from backend.extensions import db, login_manager

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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    app.run(debug=True)