from flask import Flask, render_template, request, redirect, url_for, send_file, session
from flask_sqlalchemy import SQLAlchemy
from collections import Counter
import re
import pymssql
import csv
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/azureuser/flaskapp/users.db'
app.config['SECRET_KEY'] = 'dummy_key'
db = SQLAlchemy(app)
# Variables for the Retail Customer Trends database
trends_server = 'retailcustomertrends.database.windows.net'
trends_user = 'cloudcomputeradmin'
trends_password = 'cloudisfun123!'
trends_database = 'RetailCustomerTrends'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)

with app.app_context():
    db.create_all()

def query_customer_trends(query, data, attempt=1):
    conn = None
    try:
        # Connect to the database
        conn = pymssql.connect(server=trends_server, user=trends_user, password=trends_password, database=trends_database)
        print(attempt)
        # Create a cursor object
        cursor = conn.cursor()
        # Execute the query that was passed in as a parameter
        if data == "none":
            print(data)
            cursor.execute(query)
        else:
            print("executing query " + query + " with data ")
            print(tuple(data))
            cursor.execute(query, tuple(data))
        conn.commit()
        # if there is no description then we inserted and it worked, return true
        if cursor.description is None:
            cursor.close()
            conn.close()
            return "true"
        # Fetch all the records
        rows = cursor.fetchall()
        # Close the connection
        cursor.close()
        conn.close()

        # Return the result of the query as a list of rows
        return rows
    except Exception as error:
        print(error)
        if conn != None:
            conn.rollback()
        if attempt <= 3: query_customer_trends(query, data, attempt+1)
        else: return "error"

def get_search_data(query, attempt=1):
    try:
        # Connect to the database
        conn = pymssql.connect(server=trends_server, user=trends_user, password=trends_password, database=trends_database)

        # Create a cursor object
        cursor = conn.cursor()

        # Execute the query that was passed in as a parameter
        cursor.execute(query)

        # Fetch all the records
        rows = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

        # Return the result of the query as a list of rows
        return rows
    except:
        if attempt <= 2: query_customer_trends(query, attempt+1)
        else: return "error"

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
        # Add the user to the session
        session['username'] = request.form['username']
        session['firstname'] = request.form['firstname']
        session['lastname'] = request.form['lastname']
        session['email'] = request.form['email']
        return redirect(url_for('menu'))
    return render_template('register.html')

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user:
            if user.password == request.form['password']:  # In a real app, use password hashing
                # Add the user to the session
                session['username'] = user.username
                session['firstname'] = user.firstname
                session['lastname'] = user.lastname
                session['email'] = user.email
                return redirect(url_for('menu'))
            else:
                return render_template('login.html', login_failed=True)
        else:
            return render_template('login.html', login_failed=True)
    return render_template('login.html', login_failed=False)

@app.route('/logout')
def logout():
    if session:
      if session['email']: session.pop('email', None)
      if session['username']: session.pop('username', None)
      if session['firstname']: session.pop('firstname', None)
      if session['lastname']: session.pop('lastname', None)
    return redirect(url_for('home'))

# Take the user to the main menu (to choose search, upload, or dashboard)
@app.route('/menu')
def menu():
    if not session or not session['username'] or not session['firstname'] or not session['lastname'] or not session['email']: return redirect(url_for('home'))
    return render_template('menu.html')

# Helper method for generating the results table on the search page
def generate_table(hshd_num):
    query_string = f"""SELECT transactions.HSHD_NUM, BASKET_NUM, PURCHASE_DATE, products.PRODUCT_NUM, DEPARTMENT, COMMODITY, SPEND,
    UNITS, STORE_R, WEEK_NUM, YEAR, L, AGE_RANGE, MARITAL, INCOME_RANGE, HOMEOWNER, HSHD_COMPOSITION, HH_SIZE, CHILDREN
    FROM ((transactions JOIN households ON transactions.HSHD_NUM = households.HSHD_NUM) JOIN products ON transactions.PRODUCT_NUM = products.PRODUCT_NUM)
    WHERE transactions.HSHD_NUM = {str(hshd_num)} ORDER BY transactions.HSHD_NUM, BASKET_NUM, PURCHASE_DATE, products.PRODUCT_NUM, DEPARTMENT, COMMODITY"""
    query_res = get_search_data(query_string)
    if query_res == "error" or type(query_res) != list: return "error"
    table_content = ""
    for row in query_res:
      table_content += "<tr>"
      for value in row:
        table_content += "<td>" + str(value) + "</td>"
      table_content += "</tr>"
    return table_content

@app.route('/search', methods=["GET","POST"])
def search():
    if not session or not session['username'] or not session['firstname'] or not session['lastname'] or not session['email']: return redirect(url_for('home'))
    error_string = "<p style='color: red'>Unable to connect to the database. Please refresh the page and try again.</p>"
    if request.method == "GET":
      table_content = generate_table(10)
      if table_content == "error": return render_template('search.html', table_content=error_string, error=True)
      return render_template('search.html', table_content=table_content, error=False)
    else:
      table_content = generate_table(request.form['hshd_num_input'])
      if table_content == "error": return render_template('search.html', table_content=error_string, error=True)
      if len(table_content) == 0: return render_template('search.html', table_content="<p style='color: red'>No data found.</p>", error=True)
      return render_template('search.html', table_content=table_content, error=False)

@app.route('/dashboard')
def dashboard():
    if not session or not session['username'] or not session['firstname'] or not session['lastname'] or not session['email']: return redirect(url_for('home'))
    return render_template('dashboard.html')


def insert_data(data, table):
    transactions = "INSERT INTO transactions (BASKET_NUM, HSHD_NUM, PURCHASE_DATE, PRODUCT_NUM, SPEND, UNITS, STORE_R, WEEK_NUM, YEAR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    households = "INSERT INTO households (HSHD_NUM, L, AGE_RANGE, MARITAL, INCOME_RANGE, HOMEOWNER, HSHD_COMPOSITION, HH_SIZE, CHILDREN) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    products = "INSERT INTO products (PRODUCT_NUM, DEPARTMENT, COMMODITY, BRAND_TY, NATURAL_ORGANIC_FLAG) VALUES (%s, %s, %s, %s, %s)"
    queries = [transactions, households, products]
    for row in data:
        query = queries[int(table)]
        query_res = query_customer_trends(query, row)
        if query_res == "error": return "false"
    return "true"


@app.route('/upload', methods=['GET','POST'])
def upload():
    if not session or not session['username'] or not session['firstname'] or not session['lastname'] or not session['email']: return redirect(url_for('home'))
    if request.method == "POST":
        file = request.files['file_upload']
        table = request.form['data_type']
        if file:
            data = file.read().decode('utf-8')
            parsed_data = csv.reader(data.splitlines(), delimiter=',')
            next(parsed_data, None)
            successful = insert_data(list(parsed_data), table)
            return render_template('upload.html', success=successful)
        return render_template('upload.html', success="true")
    return render_template('upload.html', success="none")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
