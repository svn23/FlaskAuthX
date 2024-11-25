from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory, flash
import os
import logging
import mysql.connector
import bcrypt
from flask_cors import CORS
from functools import wraps
from flask import session, redirect, url_for
from flask import Flask, session, redirect, url_for, render_template, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Function to read the session key from Session.txt
def get_session_key():
    try:
        file_path = 'Session.txt'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read().strip()  # Read and return the session key
        else:
            raise FileNotFoundError(f"The file {file_path} does not exist.")
    except Exception as e:
        logger.error(f"Error reading session key from file: {str(e)}")
        raise e
@app.route('/reset_page', methods=['GET'])
def reset_page():
    return render_template('reset_page.html')

def login_required(f):
    @wraps(f)  # This will preserve the original function's name and docstring
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))  # Redirect to login if not logged in
        return f(*args, **kwargs)
    return wrap
# Set the secret_key for the Flask app
app.secret_key = get_session_key()

# Database connection function
def connect_to_database():
    return mysql.connector.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )
@app.route('/create-user', methods=['POST'])
def create_user():
    try:
        # Retrieve data from the request
        avatar = request.files.get('avatar')  # Optional field
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        age = request.form.get('age', '').strip()
        role = request.form.get('role', '').strip()
        password = request.form.get('password', '')
        retype_password = request.form.get('retypePassword', '')

        # Validate required fields
        if not all([name, email, age, password, retype_password, role]):
            return jsonify({"error": "All fields except avatar are required"}), 400

        if password != retype_password:
            return jsonify({"error": "Passwords do not match"}), 400

        try:
            age = int(age)
        except ValueError:
            return jsonify({"error": "Age must be a valid number"}), 400

        # Hash the password using bcrypt
        hashed_password = hash_password(password).decode('utf-8')

        # Save the data to the database
        connection = connect_to_database()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO users (name, email, age, password, role)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (name, email, age, hashed_password, role)
            )
            connection.commit()
            user_id = cursor.lastrowid
            return jsonify({"success": True, "message": "User created successfully!"}), 201
            return redirect(url_for('admin_dash', user_id=user_id))
        except mysql.connector.IntegrityError as err:
            if err.errno == 1062:  # Duplicate entry for email
                return jsonify({"error": "Email already exists"}), 400
            raise
        finally:
            cursor.close()
            connection.close()

    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
# Create the users table if it doesn't exist
def create_users_table():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        age INT,
        password VARCHAR(255),
        role VARCHAR(50) DEFAULT 'standard'
    )
    """)
    connection.commit()
    cursor.close()
    connection.close()

# Hash password
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

# Verify password
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('register.html')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/signup-admin', methods=['GET', 'POST'])
def signup_admin():
    if request.method == 'GET':
        return render_template('signup_admin.html')  # Serve the create user form page
    elif request.method == 'POST':
        # Handle user creation here
        avatar = request.files.get('avatar')
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        role = request.form['role']
        password = request.form['password']

        # You can process the form data, save the user, handle the avatar, etc.
        # For example, save user to database

        # After saving, redirect to the admin dashboard
        flash('User created successfully!', 'success')
        return redirect(url_for('admin_dashboard')) 
    
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json() if request.is_json else {
            'email': request.form.get('email'),
            'password': request.form.get('password')
        }

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"success": False, "error": "Email and password are required"}), 400

        # Fetch user by email
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, age, password, role FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and verify_password(password, user['password']):
            # Set the session
            session['user_id'] = user['id']  # Storing user ID in session
            session['role'] = user['role']  # Store role to control access

            # Redirect based on the role
            if user['role'] == 'admin' or user['role'] == 'Admin':
                return redirect(url_for('admin_dashboard', user_id=user['id']))
            elif user['role'] == 'standard' or user['role'] == 'Standard':
                return redirect(url_for('user_dashboard', user_id=user['id']))
            else:
                return jsonify({"success": False, "error": "Unknown role"}), 403
        else:
            return jsonify({"success": False, "error": "Invalid email or password"}), 401

    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return jsonify({"success": False, "error": "An unexpected error occurred"}), 500


@app.route('/update-roles', methods=['POST'])
@login_required
def update_roles():
    try:
        updated_roles = request.get_json()

        # Connect to the database
        connection = connect_to_database()
        cursor = connection.cursor()

        # Update the role for each user
        for role_data in updated_roles:
            user_id = role_data['userId']
            new_role = role_data['selectedRole']
            cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"success": True, "message": "Roles updated successfully"}), 200

    except Exception as e:
        logger.error(f"Error updating roles: {str(e)}")
        return jsonify({"success": False, "error": "An error occurred while updating roles"}), 500

@app.route('/update-users', methods=['POST'])
@login_required
def update_users():
    try:
        updated_users = request.get_json()
        
        connection = connect_to_database()
        cursor = connection.cursor()
        
        for user in updated_users:
            cursor.execute("""
                UPDATE users 
                SET name = %s, email = %s, age = %s, role = %s 
                WHERE id = %s
            """, (user['userName'], user['userEmail'], user['userAge'], user['userRole'], user['userId']))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"message": "Users updated successfully"}), 200
    except Exception as e:
        logger.error(f"Error updating users: {str(e)}")
        return jsonify({"error": "An error occurred while updating user data"}), 500

@app.route('/update-user', methods=['POST'])
@login_required
def update_user():
    try:
        user_id = session.get('user_id')  # Get the logged-in user's ID from the session
        updated_data = request.get_json()

        # Check if age and name are provided in the request body
        name = updated_data.get('name')
        age = updated_data.get('age')

        # Validate the provided data
        if not name or not age:
            return jsonify({"error": "Name and age are required"}), 400

        # Connect to the database
        connection = connect_to_database()
        cursor = connection.cursor()

        # Update the user information in the database
        cursor.execute("""
            UPDATE users
            SET name = %s, age = %s
            WHERE id = %s
        """, (name, age, user_id))

        # Commit the changes and close the connection
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "User data updated successfully"}), 200

    except Exception as e:
        logger.error(f"Error updating user data: {str(e)}")
        return jsonify({"error": "Failed to update user data"}), 500


@app.route('/delete-user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        
        # Delete user from database
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        return jsonify({"error": "An error occurred while deleting the user"}), 500

@app.route('/reset-password/<int:user_id>', methods=['POST'])
@login_required
def reset_password(user_id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        
        # Logic to reset password (e.g., generate a new password or send an email)
        cursor.execute("SELECT email FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Send reset email or generate new password logic
        # For simplicity, we'll just log it and send a mock email
        logger.info(f"Password reset for user {user_id}, email: {user['email']}")
        
        cursor.close()
        connection.close()
        
        return jsonify({"message": "Password reset email sent"}), 200
    except Exception as e:
        logger.error(f"Error resetting password: {str(e)}")
        return jsonify({"error": "An error occurred while resetting password"}), 500


@app.route('/admin_dash/<int:user_id>')
@login_required
def admin_dashboard(user_id):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, age, role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user:
        return render_template('admin_dash.html', user=user)
    else:
        return jsonify({"error": "User not found"}), 404

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)  # Remove user ID from session
#     session.pop('role', None)  # Remove role from session
#     return redirect(url_for('login_page'))  # Redirect to login page

# Your imports...

@app.route('/logout', methods=['POST'])
def logout():
    try:
        session.pop('user_id', None)  # Remove user_id from session, logging the user out
        return redirect(url_for('login_page'))  # Flask will handle the redirection to the login page
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        return jsonify({"error": "An error occurred while logging out"}), 500

@app.route('/user_dash/<int:user_id>')
@login_required
def user_dashboard(user_id):
    # Fetch user details by ID, or additional info if needed
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, age, role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user:
        return render_template('user_dash.html', user=user)
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json() if request.is_json else {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'age': request.form.get('age'),
            'password': request.form.get('password')
        }

        name = data.get('name')
        email = data.get('email')
        age = data.get('age')
        password = data.get('password')

        if not all([name, email, age, password]):
            return jsonify({"success": False, "error": "All fields are required"}), 400

        try:
            age = int(age)
        except ValueError:
            return jsonify({"success": False, "error": "Age must be a valid number"}), 400

        # Hash the password
        hashed_password = hash_password(password)

        # Save user to the database
        connection = connect_to_database()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email, age, password, role) VALUES (%s, %s, %s, %s, %s)",
                (name, email, age, hashed_password.decode('utf-8'), 'standard')
            )
            connection.commit()
            user_id = cursor.lastrowid
            return jsonify({"success": True, "message": "Registration successful", "redirect_url": url_for('login_page')}), 201
        except mysql.connector.Error as err:
            if err.errno == 1062:  # Duplicate email
                return jsonify({"success": False, "error": "Email is already registered"}), 400
            return jsonify({"success": False, "error": f"Database error: {str(err)}"}), 500
        finally:
            cursor.close()
            connection.close()

    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        return jsonify({"success": False, "error": "An unexpected error occurred"}), 500




# Create a logger instance
logger = logging.getLogger(__name__)

@app.route('/api/users', methods=['GET'])
@login_required  # Ensure only authorized users can access this
def get_all_users():
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        
        # Query to fetch all users
        cursor.execute("""
            SELECT id, name, email, age, role 
            FROM users
        """)
        
        users = cursor.fetchall()

        cursor.close()
        connection.close()

        if users:
            return jsonify(users), 200
        else:
            return jsonify({"error": "No users found"}), 404

    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        return jsonify({"error": "Failed to fetch users"}), 500

@app.route('/api/user', methods=['GET'])
@login_required  # Ensure the user is logged in before accessing the data
def api_get_user():
    try:
        # Get the logged-in user's ID from the session
        user_id = session.get('user_id')

        # Connect to the database
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        
        # Query the user data from the database, excluding profile_picture
        cursor.execute("""
            SELECT id, name, email, age, role
            FROM users
            WHERE id = %s
        """, (user_id,))
        
        # Fetch the user data
        user = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # If the user is found, return the user data as JSON
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        logger.error(f"Error fetching user data: {str(e)}")
        return jsonify({"error": "Failed to fetch user data"}), 500


@app.route('/users/<email>', methods=['GET'])
def get_user_by_email(email):
    try:
        connection = connect_to_database()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, age, role FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code=404, error_message="Page Not Found", error_description="The page you are looking for does not exist."), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500, error_message="Internal Server Error", error_description="An unexpected error occurred."), 500

if __name__ == '__main__':
    create_users_table()
    app.run(debug=True, port=5001)