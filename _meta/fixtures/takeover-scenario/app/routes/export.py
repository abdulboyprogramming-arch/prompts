"""CSV export for one report."""
import csv
import io

from flask import Blueprint, Response

from . import _query

export_bp = Blueprint("export", __name__)


@export_bp.get("/reports/<int:report_id>/export.csv")
def export(report_id):
    rows = _query("SELECT id, payload FROM reports WHERE id = %s", (report_id,))
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "payload"])
    writer.writerows(rows)
    return Response(buf.getvalue(), mimetype="text/csv")


# def export(report_id, fmt="xlsx"):
#     # earlier version, kept in case the CSV one is wrong
#     ...
