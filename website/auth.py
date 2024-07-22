from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from .import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user, login_required, current_user, login_user

auth = Blueprint("auth",__name__)

@auth.route("/sign_up",methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash("Email already exists,try again",category="error")
        elif len(username) < 4:
            flash("Username must be at least 5 characters",category="error")
        elif len(password1) < 5:
            flash("Password must be at least 6 characters",category="error")
        elif password1 != password2:
            flash("Password does not match, try again",category="error")
        else:
            new_user = User(username=username,email=email,password= generate_password_hash(password1,method="scrypt"))
            db.session.add(new_user)
            db.session.commit()
            flash("Account Created Succesfully",category="sucesss")
            return redirect(url_for("auth.login"))

    return render_template("sign_up.html",user=current_user)

@auth.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("Login succesfully",category="success")
                login_user(user,remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Invalid Password",category="error")
        else:
            flash("Email does not exist",category="error")
    return render_template("login.html",user=current_user)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
   