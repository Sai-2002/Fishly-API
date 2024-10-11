from flask import Flask
from flask_cors import CORS

# directory imports
# from src.db.setup_db import setup 
from src.routes.products.products import products 
from src.routes.login.login import login_blue
from src.routes.admin.admin import admin

def create_app():
    app = Flask(__name__)
    app.config['session_secret'] = "Temporary secret"
    # app['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)

    CORS(app)

    app.register_blueprint(products)
    app.register_blueprint(login_blue)
    app.register_blueprint(admin)

    @app.route("/")
    def home():
        return "Home"
    
    return app

if __name__ == "__main__":
    app = create_app()
    # setup()
    app.run(debug = True)
