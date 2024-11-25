import secrets
import base64


# Generate a random secret key
secret_key = base64.b64encode(secrets.token_bytes(24)).decode('utf-8')

# Path to the session key file
file_path = 'Session.txt'

# Check if the file exists, and write the new secret key to it
try:
    # If the file exists, open it and overwrite the content
    with open(file_path, 'w') as file:
        file.write(secret_key)
    print(f"New secret key generated and saved in {file_path}: {secret_key}")
except Exception as e:
    print(f"An error occurred while saving the secret key: {e}")
