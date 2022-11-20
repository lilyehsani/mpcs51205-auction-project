from flask import Flask

from flaskr.container.dependency_container import Module
from flaskr.router import account_routes

app = Flask(__name__)

app.register_blueprint(account_routes.blueprint, url_prefix="/account")

if __name__ == "__main__":
    di = Module()
    di.wire(modules=[
        account_routes
    ])

    app.run(debug=True)
