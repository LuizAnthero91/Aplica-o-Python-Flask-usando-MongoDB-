from flask import Flask
from routes.category_routes import category_bp

app = Flask(__name__)

app.register_blueprint(category_bp)

if __name__ == "__main__":
    app.run(debug=True)
