
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from example.db import get_db

data = Blueprint("api", __name__, url_prefix="/data")


@data.route("/data", methods=("POST",))
def create_data():
    """Create data."""
    
    form = request.form.copy().to_dict()
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute( # INSERT SQL command
            """
            """,
            form,
        )
        db.commit()
    except db.ProgrammingError:
        return "Missing data parameter.", 400
    except db.IntegrityError:
        return "Invalid data parameter.", 400
    else:
        return "Data successfully created.", 201


@data.route("/data/<int:id>", methods=("GET",))
def read_data(id: int):
    """Read data."""

    db = get_db()
    row = db.execute("SELECT * FROM data WHERE id = ?", (id,)).fetchone()
    if not row:
        return "Data does not exist.", 404
    return dict(row)


@data.route("/data/<int:id>", methods=("PUT",))
def update_data(id: int):
    """Update data."""
    
    form = request.form.copy().to_dict()
    form["id"] = id
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute( # UPDATE SQL command
            """
            """,
            form,
        )
        db.commit()
    except db.ProgrammingError:
        return "Missing data parameter.", 400
    except db.IntegrityError:
        return "Invalid data parameter.", 400
    else:
        return "Data successfully updated.", 201


@data.route("/data/<int:id>", methods=("DELETE",))
def delete_data(id: int):
    """Delete data."""

    db = get_db()
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("DELETE FROM data WHERE id = ?", (id,))
    db.commit()
    return "Data successfully deleted.", 200

