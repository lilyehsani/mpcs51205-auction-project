from flask import Flask

from flaskr.container.dependency_container import Module
from flaskr.router import account_routes
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager
import datetime

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWTManager(app)  # initialize JWTManager
app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)  # define the life span of the token


app.register_blueprint(account_routes.blueprint, url_prefix="/account")

if __name__ == "__main__":
    di = Module()
    di.wire(modules=[
        account_routes
    ])

    app.run(debug=True, host='0.0.0.0')
