from flask import Flask

from sqlalchemy import create_engine
from tshistory.api import timeseries
from tshistory_rest.blueprint import blueprint as rest_blueprint

from tsview.blueprint import tsview
from tsview.history import historic


app = Flask('tsview')


def kickoff(host, port, dburi, handler, debug=False):
    engine = create_engine(dburi)
    app.register_blueprint(
        rest_blueprint(
            timeseries(
                dburi,
                handler=handler
            )
        ),
        url_prefix='/api'
    )
    app.register_blueprint(
        tsview(
            engine,
            has_permission=lambda perm: True
        )
    )
    historic(app, timeseries(dburi))
    app.run(host=host, port=port, debug=debug, threaded=not debug)
