from flask import Blueprint, request, redirect
from flask_login import login_required
review_bp = Blueprint("review", __name__)

@review_bp.route("/add-review", methods=["POST"])
@login_required
def add_review():

    image = request.files.get("image")

    if image:
        path = "frontend/static/images/reviews/" + image.filename
        image.save(path)

    return redirect(request.referrer)