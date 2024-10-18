from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta

# directory imports
# from src.db.setup_db import setup 
from src.routes.products.products import products 
from src.routes.login.login import login_blue
from src.routes.admin.admin import admin
from src.routes.payment.payment import payment

def create_app():
    app = Flask(__name__)
    app.config['session_secret'] = "Temporary secret"
    app.config['JWT_SECRET_KEY'] = "JWT_SECRET"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=3)
    # app['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)

    CORS(app)

    jwt = JWTManager(app=app)

    app.register_blueprint(products)
    app.register_blueprint(login_blue)
    app.register_blueprint(admin)
    app.register_blueprint(payment)

    @app.route("/")
    def home():
        return "Home"
    
    return app

if __name__ == "__main__":
    app = create_app()
    # setup()
    app.run(debug = True)
