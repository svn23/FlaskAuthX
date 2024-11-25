# Security Policy

This project is built with Flask as the backend and MySQL as the database. Given the nature of this application, we are handling sensitive user data such as passwords, emails, and roles. It is crucial to follow security best practices to protect user information and ensure the safety of the application.

### Authentication and Authorization
- **Login and Session Management:** 
  - Sessions are used to authenticate users. We use Flask’s `session` object to store user information after login (such as user ID and role).
  - The session secret key is dynamically loaded from a file called `Session.txt`. Ensure this file is properly secured and not accessible to unauthorized users.
  - Passwords are securely hashed using the bcrypt library before being stored in the database.

- **Role-based Access Control (RBAC):** 
  - Roles such as 'admin' and 'standard' users are assigned during user creation and are used to control access to different parts of the application.
  - Only admins have access to specific routes like `/admin_dash`, and users can only access their own data or their authorized data.

### Sensitive Data Handling
- **Password Hashing:** 
  - All user passwords are hashed using bcrypt before they are stored in the database to prevent plain-text password storage.
  - When users attempt to log in, their entered password is hashed and compared with the stored hash to verify authentication.

- **Database Security:**
  - Always ensure your MySQL database is configured with the correct permissions, only allowing access to authorized users.
  - Use parameterized queries to prevent SQL injection attacks (e.g., using `cursor.execute()` with parameters rather than interpolating variables directly into queries).
  
- **Secure Communication:** 
  - **TLS/SSL:** Use HTTPS to encrypt communication between the client and server to prevent interception of sensitive data (like passwords).
  - **CORS Protection:** CORS (Cross-Origin Resource Sharing) is enabled to control which domains can interact with the API. Only trusted domains should be allowed.

### Input Validation and Sanitization
- **Input Validation:** 
  - User input is validated both on the client-side (in the HTML forms) and server-side (in the Python backend) to prevent malicious data from being processed.
  - Age is validated to ensure it is an integer, and passwords are compared to ensure they match before submission.
  - Ensure that all form data, particularly email and name, are sanitized before processing and inserting into the database to avoid malicious scripts (XSS attacks).

### Error Handling
- **Error Handling:** 
  - Proper error handling is in place to catch and log unexpected errors using the Python `logging` module.
  - Custom error pages are provided for 404 (not found) and 500 (internal server error) statuses to inform users about issues.
  
### Security Best Practices
- **Logging:** 
  - Logs are created for all critical actions (e.g., user login attempts, role updates, etc.) to track any suspicious activity.
  - Make sure the log files are properly secured and access is limited to authorized personnel only.

- **Secret Management:** 
  - The `secret_key` for the Flask app is retrieved from a file (`Session.txt`). Ensure this file is properly protected from unauthorized access.
  - Never hard-code sensitive information like database credentials or session secrets directly in the code. Consider using environment variables or a secrets management service.

### Vulnerabilities to Watch Out For
- **SQL Injection:** Always use parameterized queries or ORM libraries to interact with the database, never interpolate user data directly into SQL queries.
- **Cross-Site Scripting (XSS):** Ensure that user-generated content (e.g., name, email) is properly sanitized before being rendered in HTML templates.
- **Cross-Site Request Forgery (CSRF):** If you are working with forms that modify data (e.g., login, create user), consider adding anti-CSRF tokens to protect against this attack.
- **Broken Authentication:** Ensure that session management and login mechanisms are properly configured to avoid attacks such as session fixation or brute-force login attempts.

### Vulnerability Disclosure
If you believe you have discovered a security vulnerability in this application, please contact the project maintainers directly at `contact@example.com`. Do **not** disclose the vulnerability publicly until it has been addressed to ensure the security of the application and its users.

### Updating Dependencies
- Ensure that all dependencies are kept up-to-date to prevent known vulnerabilities in libraries such as Flask, bcrypt, and MySQL connectors.
- Use dependency management tools like `pip freeze` to lock versions and ensure compatibility across environments.

### Recommendations for Deployment
- For production environments, ensure that the Flask app is run behind a WSGI server like Gunicorn or uWSGI, and proxy through a web server like Nginx or Apache.
- Consider using a cloud-based database with automatic backups and multi-region support to enhance security and availability.
- Always monitor your application for unusual activity or potential attacks, and ensure proper access controls are in place for all services.


## Reporting a Vulnerability

You can report vulnerability at sovanmstse@gmail.com
