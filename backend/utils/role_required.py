from functools import wraps
from flask_login import current_user
from flask import redirect

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.role != role:
                return redirect("/")
            return func(*args, **kwargs)
        return wrapper
    return decorator