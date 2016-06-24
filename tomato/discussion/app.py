# -*- coding: utf-8 -*-

import logging

import click
from flask import Flask

from tomato.discussion.core import db
from tomato.discussion.core import jsonrpc
from tomato.discussion import transactions

def create_app():
    app = Flask(__name__)

    app.config.from_object('tomato.discussion.settings')
    app.config.from_envvar('DISCUSSION_SETTINGS', silent=True)
    print('Running application in %s mode' % (app.debug and 'DEBUG' or 'NON-DEBUG'))

    db.app = app
    db.init_app(app)

    jsonrpc.app = app
    jsonrpc.init_app(app)

    register_cli(app)

    return app

def register_cli(app):
    @app.cli.group(name='db')
    def cli_db():
        pass

    @cli_db.command()
    def init():
        from tomato.discussion import models
        db.create_all()
