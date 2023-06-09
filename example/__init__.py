#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from os import makedirs

from flask import Flask
from dash import Dash
from dash import page_registry

from example.api.data import data
from example.db import init_app
from example.layout.default import layout


def create_app(test_config=None):
    """Instantiate Dash and Flask API."""
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        MAX_CONTENT_LENGTH=16000000, #16MB
        SECRET_KEY="dev",
        DATABASE=path.join(app.instance_path, "data.sqlite"),
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)
    try:
        makedirs(app.instance_path)
    except OSError:
        pass
    init_app(app)
    app.register_blueprint(data)
    dashapp = Dash(
        __name__,
        server=app,
        use_pages=True,
        update_title=None,
    )
    values = page_registry.values()
    dashapp.layout = layout(values)
    return dashapp.server
