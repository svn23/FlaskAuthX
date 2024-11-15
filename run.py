from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
import os
import logging
import requests
from flask_cors import CORS
import bcrypt

app = Flask(__name__)
CORS(app)

# Only allow requests from localhost:3000
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5000"}})

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:5000"  # The backend API URL

def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/x-icon')


def get_user_by_email(email):
    """
    Fetch user by email from the backend API.
    """
    try:
        response = requests.get(f"{API_URL}/users/{email}")

        if response.status_code == 200:
            return response.json()  # Assuming response is a JSON object with user data
        else:
            return None  # If user not found or error in fetching
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching user from backend: {str(e)}")
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('register.html')


@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/signup', methods=['POST'])
def signup():
    try:
        logger.debug("Received signup request")
        logger.debug(f"Content-Type: {request.headers.get('Content-Type')}")

        # Handle JSON data
        if request.is_json:
            data = request.get_json()
            logger.debug(f"Received JSON data: {data}")
        else:
            data = request.form.to_dict()
            logger.debug(f"Received form data: {data}")

        # Validate required fields
        required_fields = ['name', 'email', 'age', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"success": False, "error": f"{field} is required"}), 400

        # Convert age to integer
        try:
            age = int(data['age'])
        except ValueError:
            return jsonify({"success": False, "error": "Age must be a valid number"}), 400

        # Check if user already exists by email
        existing_user = get_user_by_email(data['email'])
        if existing_user:
            return jsonify({"success": False, "error": "Your account is already present, kindly login."}), 400

        # Prepare user data
        user_data = {
            "name": data['name'],
            "email": data['email'],
            "age": age,
            "password": data['password']  # Don't forget to hash password before saving in production!
        }

        logger.debug(f"Sending data to backend: {user_data}")

        # Make request to backend API to save the new user
        response = requests.post(
            f"{API_URL}/users",
            json=user_data,
            headers={'Content-Type': 'application/json'}
        )

        logger.debug(f"Backend response status: {response.status_code}")
        logger.debug(f"Backend response content: {response.text}")

        if response.status_code == 201:
            success_response = {
                "success": True,
                "message": "Registration successful",
                "redirect_url": url_for('login_page')
            }
            return jsonify(success_response), 201
        else:
            error_message = response.json().get("error", "Registration failed")
            return jsonify({"success": False, "error": error_message}), response.status_code

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return jsonify({"success": False, "error": "Failed to connect to backend service"}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"success": False, "error": "An unexpected error occurred"}), 500

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
            logger.error("Email or Password is missing")
            return jsonify({"success": False, "error": "Email and password are required"}), 400

        # Use the get_user_by_email function to fetch user data from the backend API
        user = get_user_by_email(email)

        if user:
            # Encode the password entered by the user
            encoded_password = password.encode('utf-8')  # Encode the entered password to UTF-8
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())  # Hash the encoded password

            # Compare the hashed password with the stored hash
            if bcrypt.checkpw(encoded_password, user['password'].encode('utf-8')):
                return jsonify({
                    "success": True,
                    "message": "Login successful",
                    "redirect_url": url_for('index')  # Redirect to homepage or dashboard
                }), 200
            else:
                logger.error(f"Invalid password for user: {email}")
                return jsonify({"success": False, "error": "Invalid credentials"}), 400
        else:
            logger.error(f"User not found: {email}")
            return jsonify({"success": False, "error": "User not found"}), 404

    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return jsonify({"success": False, "error": "An unexpected error occurred"}), 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html',
                           error_code=404,
                           error_message="Page Not Found",
                           error_description="The page you are looking for does not exist."), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html',
                           error_code=500,
                           error_message="Page Not Found",
                           error_description="The page you are looking for does not exist."), 500


@app.errorhandler(403)
def forbidden(error):
    return render_template('error.html',
                           error_code=403,
                           error_message="Forbidden",
                           error_description="You are not authorized to access this resource."), 403


@app.errorhandler(400)
def bad_request (error):
    return render_template('error.html',
                           error_code=400,
                           error_message="Bad Request",
                           error_description="The request could not be understood by the server due to malformed syntax."), 400




if __name__ == '__main__':
    app.run(debug=True, port=5001)
