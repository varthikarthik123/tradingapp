# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app, origins="http://localhost:4200")  # Enable CORS for all routes

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nagatejith1@",
    database="stock_trade",
)

# Use a context manager to handle the cursor, ensuring it's properly closed
def execute_query(query, params=None):
    try:
        with mydb.cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        return result
    except Exception as e:
        raise e
 
    
@app.route('/verify_login', methods=['POST'])
def verify_login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        print(f"Received email: {email}")
        print(f"Received password: {password}")

        query = "SELECT * FROM customers WHERE email=%s AND password=%s"
        result = execute_query(query, (email, password))

        if result:
            return jsonify({"success": True, "message": "Login successful"})
        else:
            return jsonify({"success": False, "message": "Invalid username or password"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        phonenumber = data.get('phonenumber')
        password = data.get('password')
        

        # Check if the email, username, or phone number is already registered
        check_query = "SELECT * FROM customers WHERE email=%s OR username=%s OR phonenumber=%s"
        existing_user = execute_query(check_query, (email, username, phonenumber))

        if existing_user:
            return jsonify({"success": False, "message": "One or more details already registered"})

        # Insert new user into the database
        #insert_query = "INSERT INTO customers (email, username, phonenumber, password) VALUES (%s, %s, %s, %s)"
        #print(f"insert Query: { insert_query }")
        #execute_query(insert_query, (username, email, phonenumber, password))
        insert_query = "INSERT INTO customers (email, username, phonenumber, password) values (%s, %s, %s, %s)"
        execute_query(insert_query, (email, username, phonenumber, password))
        mydb.commit()
        return jsonify({"success": True, "message": "Signup successful"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
