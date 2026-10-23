"""HTTP routes. Queries are inline SQL strings."""
import os

from flask import Blueprint, jsonify

bp = Blueprint("main", __name__)


@bp.get("/reports/<int:user_id>")
def reports_for_user(user_id):
    # Fails against a fresh database: reports has no user_id column (see schema.sql).
    sql = "SELECT id, user_id, payload FROM reports WHERE user_id = %s"
    rows = _query(sql, (user_id,))
    return jsonify([{"id": r[0], "user_id": r[1], "payload": r[2]} for r in rows])


@bp.get("/health")
def health():
    return {"ok": True}


def _query(sql, params):
    import psycopg2

    dsn = os.environ["DATABASE_URL"]
    with psycopg2.connect(dsn) as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def _fmt_date(value):
    return value.strftime("%Y-%m-%d")
