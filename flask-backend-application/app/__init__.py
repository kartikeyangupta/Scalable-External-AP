import logging

from flask import Flask, request as req

from app.controllers import pages
import config
from app.extentions import db
from make_celery import celery


def create_app(config_filename=config):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    db.init_app(app)
    app.register_blueprint(pages.blueprint)

    app.logger.setLevel(logging.NOTSET)

    @app.after_request
    def log_response(resp):
        app.logger.info("{} {} {}\n{}".format(
            req.method, req.url, req.data, resp)
        )
        return resp

    return app
