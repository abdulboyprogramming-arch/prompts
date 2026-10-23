"""Reportwright-lite. Entry point: python -m app.main"""
from flask import Flask

from .config import load_config
from .routes import bp
from .routes.export import export_bp

app = Flask(__name__)
app.register_blueprint(bp)
app.register_blueprint(export_bp)


def create():
    cfg = load_config()
    app.config.update(cfg)
    return app


if __name__ == "__main__":
    create().run(host="0.0.0.0", port=8080)
