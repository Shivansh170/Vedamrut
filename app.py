from flask import Flask, redirect, render_template, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SECRET_KEY'] = "0009563e8b7171e4ddba20632e23afe9"
db = SQLAlchemy(app)
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return f"username->{self.username}"
with app.app_context():
    db.create_all()
@app.route("/")
def home():
    return f"Welcome to the homepage!!"
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form["username"]
        if Users.query.filter_by(username=username).first():
            return render_template("signup.html", error="The username already exists in the database!!!")
        password = request.form["password"]
        new_password = generate_password_hash(password)
        newuser = Users(username=username, password=new_password)
        db.session.add(newuser)
        db.session.commit()
        flash("You have successfully created your account!")
        return redirect(url_for('home'))
    return render_template("signup.html")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        exist = Users.query.filter_by(username=username).first()
        if exist and check_password_hash(exist.password, password):
            session['user_id'] = exist.id
            session['username'] = exist.username
            return redirect(url_for('home',session=session))
        else:
            return render_template("login.html", error="Invalid username or password!")
    return render_template("login.html")
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_as_surveyor'))
if __name__=="__main__":
    app.run(debug=True)