from flask import render_template, url_for, flash, redirect, request
from RvParkApp import app, db, bcrypt
from RvParkApp.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def user_auth():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('signin-register.html')


@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/register_user" , methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        username = request.form["username"]
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        user = User.query.filter_by(email=email).first()
        user2 = User.query.filter_by(username=username).first()
        if user:
            flash("User already exists, please try logging in", "error")
            return redirect(url_for('user_auth'))
        elif user2:
            flash("User already exists, please try logging in", "error")
            return redirect(url_for('user_auth'))
        else:
            user = User(username=username.strip(), email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash('You have successfully registered','success')
            return redirect(url_for('user_auth'))


@app.route("/login_user", methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form['password']
        user = User.query.filter_by(username=username.strip()).first()
        if user:
            if str(password) == str(user.password):
                login_user(user)
                return redirect(url_for('home'))
        else:
            flash("Incorrect username or password","danger")
            print("here")
            return redirect(url_for('user_auth'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('user_auth'))