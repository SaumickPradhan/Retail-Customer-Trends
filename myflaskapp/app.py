from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from collections import Counter
import re
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ubuntu/myflaskapp/users.db'
app.config['SECRET_KEY'] = 'dummy_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)

with app.app_context():	
    db.create_all()


# routes

# landing page
@app.route('/')
def home():
    return render_template('landing.html')

# register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(
            username=request.form['username'],
            password=request.form['password'],  # In a real app, ensure to hash passwords
            firstname=request.form['firstname'],
            lastname=request.form['lastname'],
            email=request.form['email']
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('success', firstname=new_user.firstname, lastname=new_user.lastname, email=new_user.email))
    return render_template('register.html')

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user:
            if user.password == request.form['password']:  # In a real app, use password hashing
                return redirect(url_for('success', firstname=user.firstname, lastname=user.lastname, email=user.email))
            else:
                return render_template('login.html', login_failed=True)
        else:
            return render_template('login.html', login_failed=True)
    return render_template('login.html', login_failed=False)

# success
@app.route('/home')
def success():
    return render_template('home.html', auth=True)

@app.route('/download')
def download():
    return send_file('Limerick.txt', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)


