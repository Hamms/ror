# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flaskext.markdown import Markdown

def create_app(config_overrides={}):
    """Create and return an Flask app instance"""

    # create app; load config
    app = Flask(__name__)
    app.config.from_object('config')
    app.config.update(**config_overrides)

    Markdown(app)

    # error page handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template('500.html'), 500

    # register blueprints
    from app.main.views import mod as main_module

    app.register_blueprint(main_module)

    return app
