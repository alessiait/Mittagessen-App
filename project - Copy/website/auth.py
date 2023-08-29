from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Erfolgreich angemeldet', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.manage_appointments'))

            else:
                flash('Password ist falsch.', category='error')
        else:
            flash('Email existiert nicht', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        place = request.form.get('place')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email wurde schon registriert', category='error')
        elif len(email) < 4:
            flash('Email sollte länger als 3 Zeichen sein.', category='error')
        elif len(first_name) < 1:
            flash('Vorname sollte länger als 1 Zeichen sein.', category='error')
        elif len(first_name) < 1:
            flash('Nachname sollte länger als 1 Zeichen sein.', category='error')
        elif password1 != password2:
            flash('Passwords sind nicht gleich.', category='error')
        elif len(password1) < 7:
            flash('Password sollte länger als 7 Zeichen sein.', category='error')
        else:
            new_user = User(email=email, last_name=last_name, first_name=first_name, place=place, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Email registriert!', category='success')
            return redirect(url_for('views.home1'))
    
    return render_template("sign_up.html", user=current_user)

