
# User Management System with Flask

This project is a User Management System built using Flask as the backend framework, MySQL as the database, and HTML/CSS/JS for the frontend. The application allows for the creation, updating, and deletion of users, as well as password management and role-based access control. It features a secure authentication system with bcrypt for password hashing.



## :rocket:Features

* User Registration & Authentication: Users can sign up, log in, and reset their passwords.
* Admin Dashboard: Admin users can view and manage other users.
* Role Management: Admin users can update user roles.
* CRUD Operations: Admin users can create, read, update, and delete user records.
* Secure Login: Passwords are hashed using bcrypt to ensure security.
* Session Management: User sessions are securely handled using Flask's session mechanism.
* Database Integration: MySQL is used to store user data and roles.
## Deployment

To Clone this repo

```bash
  git clone https://github.com/svn23/FlaskAuthX

```
Navigate into the project directory:

```bash
  cd FlaskAuthX

```

Create a virtual environment (optional but recommended):

```bash
  python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


```

Install the required dependencies:

```bash
  pip install -r requirements.txt


```

## Setup MySQL DB
* Create a database named user_management (or any other name you'd prefer).
* Create the required table by running the create_users_table() function present in the backend.
* Update the MySQL connection details in your backend.py file (the DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, and DATABASE_NAME constants).



Run the Flask application:

```bash
  python backend.py

```

The app will run on http://127.0.0.1:5001/


## Routes
### User Routes
* GET /signup: Display the user signup page.
* POST /signup: Handle user registration.
* GET /login: Display the login page.
* POST /login: Handle user authentication.
* GET /user_dash/<user_id>: Display the user dashboard.
* POST /update-user: Update logged-in user's information.
* POST /reset-password/<user_id>: Reset password for a user.

### Admin Routes( Requires Admin Role)

* GET /admin_dash/<user_id>: Display the admin dashboard.
* POST /create-user: Create a new user.
* POST /update-roles: Update user roles.
* POST /update-users: Update multiple users at once.
* DELETE /delete-user/<user_id>: Delete a user.
* GET /api/users: Fetch all users (Admin-only access).
* GET /api/user: Fetch the logged-in user's data.

## Security Implementation

* Password Hashing: Passwords are securely hashed using bcrypt before being stored in the database.
* Session Management: Flask's session is used to manage user sessions and ensure that users are logged in before accessing certain routes.
* Role-based Access Control: Only users with the appropriate role (admin) can access certain routes, such as updating user roles or deleting users.
## Frontend

* index.html: Homepage.
* register.html: User registration form.
* login.html: User login form.
* user_dash.html: User dashboard.
* admin_dash.html: Admin dashboard.
* signup_admin.html: Admin user creation form.
## Future Update

* OIDC : Implementation of OIDC with WSO2 in local server.
* Email Notifications: Implement email functionality for password resets or notifications.
* Input Validation: Enhance frontend input validation with JavaScript or through Flask forms.
* Password Recovery: Add a feature for users to recover or reset their passwords via email.
* Advanced Search/Filtering: Provide functionality for filtering users based on role or age.
## Contributing

Contributions are always welcome!

Feel free to fork this repository and submit pull requests. If you encounter any bugs or have suggestions for improvements, open an issue on GitHub.

## License

This project is open-source and available under the
[MIT](https://choosealicense.com/licenses/mit/)
License.
