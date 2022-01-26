from flask import Flask, redirect, url_for, render_template
from database import database
from apps.scraper.views import scraper
from config import DevelopmentConfig as devconf


HOST = devconf.HOST
PORT = devconf.PORT
VERSION = devconf.VERSION


def create_app():
    ## Creating WSGI application object
    app = Flask(__name__, static_url_path='/static')

    ## Configuration
    app.config.from_object('config.DevelopmentConfig')

    ## Setup all dependencies
    database.init_app(app)

    ## Register blueprint 
    ## URL: https://HOST:PORT/api/<version>/<views>
    app.register_blueprint(scraper, url_prefix = '/api/' + VERSION)

    return app


if __name__ == '__main__':
    ## Create local variable app
    app = create_app()

    ## HTTP 404 error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404


    ## HTTP 400 error handler
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('400.html'), 400


    ## The default page
    @app.route("/")
    def got_home():
        return redirect(url_for("scraper.home"))


    ## This route can be used to check whether the application is responding or not
    @app.route('/health')
    def health():
        return "I'm Good!"


    ## Launch the application
    app.run(host=HOST, port=PORT)
