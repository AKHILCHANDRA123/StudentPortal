from getpass import getpass

from werkzeug.security import generate_password_hash


password = getpass("Admin password: ")
confirm_password = getpass("Confirm admin password: ")

if password != confirm_password:
    raise SystemExit("Passwords do not match.")

print(generate_password_hash(password))
