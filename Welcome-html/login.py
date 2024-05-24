from flask import Flask, request, render_template, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="Signup",
    password="root@1234",
    port="3306",
    auth_plugin='mysql_native_password'
)

# Check if the connection is successful
if mydb:
    print("Connected to the database")
else:
    print("Failed to connect to the database")


def logins(username, password):
    cursor = mydb.cursor()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    return user


def create_users_table():
    try:
        cursor = mydb.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL
            )
        """)
        mydb.commit()
        print("Users table created successfully")
    except Exception as e:
        print("Error creating users table:", e)

# Call function to create users table
create_users_table()

@app.route('/')
def log():
    return render_template('testtemp.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        if request.method == 'POST':
            username = request.form['User']
            password = request.form['passwords']
            email=request.form['emails']
            print(username, password, email)

            cursor = mydb.cursor()
            cursor.execute("INSERT INTO users (username, password,email) VALUES (%s, %s, %s)", (username, password, email))
            mydb.commit()
            message='Your Details have been saved'
            return render_template('testtemp.html', message=message)

    except Exception as e:
        return f'error {e}'

@app.route('/login-page', methods=['POST'])
def tth():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['password']
        result = logins(username, password)
        if result:
            return redirect(url_for('success')) # Redirect to success route
        else:
            return jsonify({'message': 'Login failed'})

@app.route('/success')
def success():
    try:
        print('its Done')
        return render_template('talent.html')
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error rendering talent.html: {e}")
        # Optionally, you can return an error page or message here
        return "An error occurred while rendering the page."

if __name__ == '__main__':
    app.run(debug=False)
