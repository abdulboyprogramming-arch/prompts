"""Reportwright — upload a CSV, get an analysis, share it by link.

Deliberately small: this fixture exists to be read, not run.
"""
from flask import Flask, render_template

app = Flask(__name__)

from routes.export import export_bp
from routes.settings import settings_bp

app.register_blueprint(export_bp)
app.register_blueprint(settings_bp)


@app.get("/r/<token>")
def report(token):
    """Reports are keyed by an unguessable token. There are no accounts."""
    return render_template("report.html", token=token)
