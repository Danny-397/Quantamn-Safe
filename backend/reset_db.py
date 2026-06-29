"""Rebuild the database schema to match the current models.

Use this when the app shows 500 errors on login/registration after the data
model changed — `db.create_all()` creates missing *tables* but never alters
existing ones, so a schema that drifted needs a rebuild.

WARNING: this DROPS all tables and recreates them — it destroys existing data.
It's intended for the pre-launch / development phase (no real users yet).

Run:
    cd backend && python reset_db.py
On Render: open the web service's "Shell" tab and run the same command.
"""

from app import create_app
from extensions import db

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database reset: all tables dropped and recreated to the current schema.")
