"""QuantumSafe backend — Flask application factory.

Run locally:
    cd backend
    flask --app app run --debug      (or: python app.py)
"""

from __future__ import annotations

import os

from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from extensions import db, jwt, limiter, mail


def create_app(config_object: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Extensions
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    app.config["RATELIMIT_STORAGE_URI"] = app.config.get("RATELIMIT_STORAGE_URI", "memory://")

    # CORS restricted to the dashboard origin(s) only, for the API surface.
    CORS(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )

    # Blueprints
    from auth import auth_bp
    from api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    # Health check
    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "service": "quantumsafe-api"})

    @app.route("/")
    def index():
        return jsonify({"service": "QuantumSafe API", "version": "v1", "docs": "/api/v1"})

    # JSON error handlers
    @app.errorhandler(404)
    def not_found(_e):
        return jsonify({"error": "Not found."}), 404

    @app.errorhandler(429)
    def ratelimited(_e):
        return jsonify({"error": "Rate limit exceeded. Slow down and try again."}), 429

    @app.errorhandler(500)
    def server_error(_e):
        return jsonify({"error": "Internal server error."}), 500

    # Create missing tables, then self-heal additive schema drift so existing
    # deployments keep working (and keep their accounts) when the model gains
    # columns — no manual migration or data wipe required.
    with app.app_context():
        db.create_all()
        _ensure_user_columns()

    return app


def _ensure_user_columns() -> None:
    """Add any columns the User model expects but the live `users` table lacks.

    db.create_all() never ALTERs existing tables, so when the model gains a
    column an older database is missing it and every login/register 500s. This
    adds the missing (additive, nullable/defaulted) columns in place, preserving
    all existing rows. Safe to run on every boot.
    """
    import logging

    from sqlalchemy import inspect, text

    try:
        insp = inspect(db.engine)
        if "users" not in insp.get_table_names():
            return
        existing = {c["name"] for c in insp.get_columns("users")}
        pg = db.engine.dialect.name == "postgresql"
        ts = "TIMESTAMP WITH TIME ZONE" if pg else "TIMESTAMP"
        true_, false_ = ("TRUE", "FALSE") if pg else ("1", "0")
        wanted = {
            "email_verified": f"BOOLEAN NOT NULL DEFAULT {false_}",
            "verification_token": "VARCHAR(64)",
            "api_key_hash": "VARCHAR(64)",
            "api_key_prefix": "VARCHAR(32)",
            "alert_on_high": f"BOOLEAN NOT NULL DEFAULT {true_}",
            "terms_accepted_at": ts,
        }
        missing = {c: ddl for c, ddl in wanted.items() if c not in existing}
        for col, ddl in missing.items():
            db.session.execute(text(f"ALTER TABLE users ADD COLUMN {col} {ddl}"))
        if missing:
            db.session.commit()
            logging.getLogger(__name__).info(
                "Schema self-heal added user columns: %s", ", ".join(missing))
    except Exception as exc:  # never let a heal attempt brick startup
        db.session.rollback()
        logging.getLogger(__name__).warning("Schema self-heal skipped: %s", exc)


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
