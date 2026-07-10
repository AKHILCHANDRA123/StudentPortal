# StudentPortal
Student Portal and Feedback Management System using Python Flask and SQLite Database

## Admin login setup

Admin credentials are configured with environment variables instead of being
stored directly in the source code.

Generate a password hash:

```bash
python generate_admin_hash.py
```

Set the variables before starting the app:

```powershell
$env:ADMIN_USERNAME = "admin"
$env:ADMIN_PASSWORD_HASH = "paste-the-generated-hash-here"
python app.py
```

On Render or another hosting platform, add `ADMIN_USERNAME` and
`ADMIN_PASSWORD_HASH` in the service environment settings.
