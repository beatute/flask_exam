import os

from flask import Flask, render_template, redirect, url_for, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, current_user, logout_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy

import forms


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = '4654f5dfadsrfasdr54e6rae'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"



association_table = db.Table('association', db.metadata,
        db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
        db.Column('actor_id', db.Integer, db.ForeignKey("actor.id"))
)

class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column("Title", db.String)
    country = db.Column("Country", db.String)
    released = db.Column("Released", db.String)
    runtime = db.Column("Runtime", db.Integer)
    about = db.Column("About", db.String)
    actors = db.relationship("Actor", secondary=association_table, back_populates="movies")

class Actor(db.Model):
    __tablename__ = "actor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String)
    surname = db.Column("Surname", db.String)
    movies = db.relationship("Movie", secondary=association_table, back_populates="actors" )


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        enc_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=enc_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('welcome'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route('/movies')
def allmovies():
    try:
        all_movies = Movie.query.all()
    except:
        all_movies = []
    return render_template('movies.html', all_movies=all_movies)

@app.route('/actors')
def allactors():
    try:
        all_actors = Actor.query.all()
    except:
        all_actors = []
    return render_template('actors.html', all_actors=all_actors)


if __name__ == '__main__':
    db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)