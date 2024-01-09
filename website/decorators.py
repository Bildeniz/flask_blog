from functools import wraps
from flask import session, redirect, url_for, request, flash

def loged_out_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' in session.keys():
            flash("You're already logged in!", 'danger')
            return redirect(url_for('views.home'))
        return f(*args, **kwargs)
    return decorated_function

def loged_in_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not ('id' in session.keys()):
            flash("You have to login!", 'danger')
            return redirect(url_for('views.home'))
        return f(*args, **kwargs)
    return decorated_function