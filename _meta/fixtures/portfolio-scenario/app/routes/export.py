"""Export routes.

CSV export exists for the summary report only. PDF export is described in the
product notes but has not been started; there is no ticket for it yet.
"""
import csv
import io

from flask import Blueprint, Response

export_bp = Blueprint("export", __name__)


@export_bp.get("/reports/<int:report_id>/export.csv")
def export_csv(report_id):
    """Only the summary table. Per-column exports are not implemented."""
    rows = _summary_rows(report_id)
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["metric", "value"])
    writer.writerows(rows)
    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f'attachment; filename="report-{report_id}.csv"'},
    )


def _summary_rows(report_id):
    # Placeholder until the analysis tables land.
    return [("rows", 0), ("columns", 0)]
