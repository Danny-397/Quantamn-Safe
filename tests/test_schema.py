"""The startup schema self-heal re-adds columns the model expects."""

import sqlite3

import pytest
from sqlalchemy import inspect, text

from app import _ensure_user_columns
from extensions import db


def _columns(app):
    with app.app_context():
        return {c["name"] for c in inspect(db.engine).get_columns("users")}


def test_self_heal_readds_missing_column(app):
    if tuple(map(int, sqlite3.sqlite_version.split("."))) < (3, 35, 0):
        pytest.skip("SQLite < 3.35 cannot DROP COLUMN")

    with app.app_context():
        db.session.execute(text("ALTER TABLE users DROP COLUMN terms_accepted_at"))
        db.session.commit()
        assert "terms_accepted_at" not in {c["name"] for c in inspect(db.engine).get_columns("users")}
        _ensure_user_columns()
        cols = {c["name"] for c in inspect(db.engine).get_columns("users")}
        assert "terms_accepted_at" in cols  # healed


def test_self_heal_drops_obsolete_column(app):
    if tuple(map(int, sqlite3.sqlite_version.split("."))) < (3, 35, 0):
        pytest.skip("SQLite < 3.35 cannot DROP COLUMN")
    with app.app_context():
        # Simulate a database left over from an older model with a `plan` column.
        db.session.execute(text("ALTER TABLE users ADD COLUMN plan VARCHAR(20)"))
        db.session.commit()
        assert "plan" in {c["name"] for c in inspect(db.engine).get_columns("users")}
        _ensure_user_columns()
        assert "plan" not in {c["name"] for c in inspect(db.engine).get_columns("users")}


def test_self_heal_is_idempotent(app):
    # Running it when nothing is missing must not error.
    with app.app_context():
        _ensure_user_columns()
        _ensure_user_columns()
