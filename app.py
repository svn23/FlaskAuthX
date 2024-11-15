from flask import Flask, request, jsonify
import mysql.connector
import bcrypt
from flask_cors import CORS  # Importing CORS for cross-origin resource sharing

app = Flask(__name__)
CORS(app)  # Enabling CORS for all routes (allows frontend to access backend)

# Connect to MySQL
def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='crud'
    )

# Create the users table if it doesn't exist
def create_users_table():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        age INT,
        password VARCHAR(255)
    )
    """)
    connection.commit()
    cursor.close()
    connection.close()

# Hash password function
# def hash_password(password):
#     salt = bcrypt.gensalt()
#     return bcrypt.hashpw(password.encode('utf-8'), salt)

# Route to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json  # Get JSON data from the frontend
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    password = data.get('password')

    if not all([name, email, age, password]):
        return jsonify({"error": "All fields are required"}), 400

    # Ensure 'age' is an integer
    try:
        age = int(age)
    except ValueError:
        return jsonify({"error": "Age must be a number"}), 400

    # hashed_password = hash_password(password)  # Hash the password before storing

    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, email, age, password) VALUES (%s, %s, %s, %s)",
            (name, email, age, password)
            # (name, email, age, hashed_password)
        )
        connection.commit()
        user_id = cursor.lastrowid
        return jsonify({"message": "User created", "user_id": user_id}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, age FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(users)

# Route to get a user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, age FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

# Route to get a user by email
# Route to get a user by email
@app.route('/users/<email>', methods=['GET'])
def get_user_by_email(email):
    try:
        # Connect to the database
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)

        # SQL query to fetch user by email
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))  # Pass email as parameter to avoid SQL injection

        user = cursor.fetchone()  # Fetch a single record

        if user:
            # User found, return user details
            return jsonify({
                "email": user['email'],
                "password": user['password']  # Return the hashed password (not plain-text)
            }), 200
        else:
            # User not found
            return jsonify({"error": "User not found"}), 404

    except mysql.connector.Error as err:
        # Handle database connection or query errors
        return jsonify({"error": f"Database error: {err}"}), 500

    finally:
        # Ensure all results are handled before closing
        if cursor:
            cursor.fetchall()  # Fetch all remaining results to clear any unread results
            cursor.close()
        if connection:
            connection.close()

# Route to update a user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    password = data.get('password')

    if not any([name, email, age, password]):
        return jsonify({"error": "At least one field is required to update"}), 400

    connection = connect_to_database()
    cursor = connection.cursor()
    update_fields = []
    update_values = []

    if name:
        update_fields.append("name = %s")
        update_values.append(name)
    if email:
        update_fields.append("email = %s")
        update_values.append(email)
    if age:
        update_fields.append("age = %s")
        update_values.append(age)
    if password:
        # hashed_password = hash_password(password)
        update_fields.append("password = %s")
        update_values.append(password)
                # update_values.append(hashed_password)

    update_values.append(user_id)
    update_query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
    
    cursor.execute(update_query, tuple(update_values))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "User updated successfully"})

# Route to delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "User deleted successfully"})

if __name__ == '__main__':
    create_users_table()  # Ensure the table is created when the server starts
    app.run(debug=True, port=5000)
