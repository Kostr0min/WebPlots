"""Initialize Flask app."""
from flask import Flask

def create_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.static_url_path = 'static'
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    @app.route("/static/<path:path>")
    def static_dir(path):
        return send_from_directory("static", path)

    with app.app_context():
        # Import parts of our core Flask app
        import routes

        # Import Dash application
        from dash_miniTablo.dashboard import init_dashboard
        app = init_dashboard(app)

        return app