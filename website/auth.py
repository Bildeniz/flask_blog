from .models import User, Article
from .decorators import loged_out_required, loged_in_required

from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from peewee import DoesNotExist, IntegrityError

from werkzeug.security import generate_password_hash, check_password_hash

"""
peewee.IntegrityError: UNIQUE constraint failed: user.email
"""

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
@loged_out_required
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')

        try:
            user = User.select().where(User.email == email).get()
        except DoesNotExist:
            flash('User not found', 'danger')
            return redirect(url_for('auth.login'))
        
        if user:
            if check_password_hash(user.password, password):
                session['id'] = user.id
                session['username'] = user.username
                session['email'] = email
                
                flash('Successfuly logged in!', 'success')
                return redirect(url_for('views.home'))
            else:
                flash('Your password is incorrect', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('User not found', 'danger')
            return redirect(url_for('auth.login'))

@auth.route('/logout')
@loged_in_required
def logout():
    session.clear()

    flash('Successfuly logged out', 'success')
    return redirect(url_for('views.home'))

@auth.route('/sign-up', methods=['POST', 'GET'])
@loged_out_required
def signUp():
    if request.method == "POST":
        username = request.form.get('username').strip()
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        passowrd_confirm = request.form.get('password-confirm')

        # Validation        
        if (len(username) < 3):
            flash('Please enter greater username', 'danger')
            return render_template('signup.html')
        elif (len(email) < 9):
            flash('Email must be greater than 9 chracters', 'danger')
            return render_template('signup.html')
        elif (password != passowrd_confirm):
            flash('Passwords not match', 'danger')
            return render_template('signup.html')
        elif (len(password)<6):
            flash('Password must be greater than 6 characters', 'danger')
            return render_template('signup.html')
        else:# Success
            passwd_hash = generate_password_hash(password=password, method='sha256')

            try:
                new_user = User(

                    username=username,
                    email=email,
                    password = passwd_hash
                )

                id = new_user.save()
            except IntegrityError:
                flash('This email address is used by another user', 'danger')
                return redirect(url_for('auth.signUp'))

            session['id'] = id
            session['username'] = username
            session['email'] = email

            flash('Account created', 'success')
            return redirect(url_for('views.home'))
    else:
        return render_template('sign_up.html')
    
@auth.route('/account')
@loged_in_required
def account():
    articles = Article.select().where(Article.user == session['id']).order_by(Article.pub_date.desc())
    for article in articles:
        print(article.title)

    return render_template('account.html', articles=articles)

@auth.route('/change-password', methods=['POST'])
@loged_in_required
def change_password():
    old_password = request.form.get('old-password')
    new_password = request.form.get('new-password')
    confirm_password = request.form.get('password-confirm')

    if new_password != confirm_password:
        flash('Passwords is not match', 'danger')
        return redirect(url_for('auth.account'))
    elif len(new_password) < 6:
        flash('Password must be greater than 6 characters', 'danger')
        return redirect(url_for('auth.account'))
    else:
        user = User.select().where(User.id == session['id']).get()

        if check_password_hash(user.password, old_password):
            hash_new_password = generate_password_hash(new_password, method='sha256')
        
            user.password = hash_new_password
            user.save()

            flash('Password is changed with successfuly', 'success')
            return redirect(url_for('auth.account'))
        else:
            flash('Password is incorrect', 'danger')
            return redirect(url_for('auth.account'))

        