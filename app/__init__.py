from flask import Flask
from config import Config
from pymongo import MongoClient

db = None

def create_app():
    app = Flask(__name__)    
    app.config.from_object('config.Config')
    global db

    try:
        client = MongoClient(app.config['MONGO_URI'])   
        db = client['stylesync']
        print("Conectado ao MongoDB com sucesso")
    except Exception as e:
        print(f'Erro ao realizar conexão com banco de dados: {e}')

    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
