from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import Post
from .import db

views = Blueprint("views",__name__)

@views.route("/")
def home():
    posts = Post.query.all()
    return render_template("home.html",user=current_user,posts=posts)

@views.route("/create-post",methods=["GET","POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title or not content:
            flash("Post cannot be empty",category="error")
        else:
            new_post = Post(title=title,content=content,user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash("Post added sucesfully",category="success")
            return redirect(url_for("views.home"))

    return render_template("create_post.html",user=current_user)
