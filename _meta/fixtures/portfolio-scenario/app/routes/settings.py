"""Settings page. The theme choice is stored; nothing reads it back yet."""
from flask import Blueprint, make_response, render_template, request

settings_bp = Blueprint("settings", __name__)


@settings_bp.get("/settings")
def settings():
    theme = request.cookies.get("theme", "system")
    return render_template("settings.html", theme=theme)


@settings_bp.post("/settings")
def save_settings():
    theme = request.form.get("theme", "system")
    response = make_response(render_template("settings.html", theme=theme))
    response.set_cookie("theme", theme, max_age=60 * 60 * 24 * 365, httponly=True)
    return response
