from backend.app import app

from backend.models.user_model import User
from backend.models.seller_model import Seller
from backend.models.product_model import Product
from backend.models.category_model import Category

if __name__ == "__main__":
    app.run(debug=True)