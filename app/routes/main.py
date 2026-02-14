from flask import Blueprint, jsonify, request, current_app
from app.models.user import LoginPayload
from pydantic import ValidationError
from app import db
from bson import ObjectId
from app.models.products import *
from app.decorators import token_required
from datetime import datetime, timedelta, timezone
import jwt


main_bp = Blueprint('main-bp',__name__)

# RF: O sistema deve permitir que um usuário se autentique para obter um token
from flask import request, jsonify, current_app
from pydantic import ValidationError
from datetime import datetime, timedelta, timezone
import jwt


@main_bp.route('/login', methods=['POST'])
def login():
    raw_data = request.get_json()
 

    if raw_data is None:
        return jsonify({"error": "Envie JSON no body e Content-Type application/json"}), 400

    try:
        user_data = LoginPayload(**raw_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    if user_data.username == 'admin' and user_data.password == "supersecret":
        token = jwt.encode(
            {
                "user_id": user_data.username,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        return jsonify({'access_token': token}), 200

    return jsonify({"mensagem": "Credenciais inválidas!"}), 401



# RF: O sistema deve permitir a listagem de todos os produtos

@main_bp.route('/products', methods= ['GET'])
def get_products():
    products_cursor = db.products.find({})
    products_list = [ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True) for product in products_cursor]
    return jsonify(products_list)

# RF: O sistema deve permitir a criação de um novo produto
@main_bp.route('/products', methods=['POST'])
@token_required
def create_product(token):
    try:
        product = Product(**request.get_json())
    except ValidationError as e:
        return jsonify({"Error": e.errors()}), 400
    
    result = db.products.insert_one(product.model_dump())
    
    return jsonify({
        "Mensagem": "Produto criado com sucesso!",
        "id": str(result.inserted_id)
    }), 201


# RF: O sistema deve permitir avisualização de um unico produto

@main_bp.route('/product/<string:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify({"error": f"Erro ao transformar em ObjectID: {e}"}), 400
    
    product = db.products.find_one({'_id': oid})

    if product:
        product['_id'] = str(product['_id'])
        return jsonify(product), 200

    return jsonify({"error": f"Produto com id {product_id} não encontrado!"}), 404



# RF: O sistema deve permitira atualização de um unico produto e produto existente
@main_bp.route('/product/<string:product_id>', methods=['PUT'])
@token_required
def update_product(token, product_id):
    return jsonify({"mensagem": f"Atualizar produto {product_id}"})


# RF: O sistema deve permitira delecao de um unico produto e produto existente
@main_bp.route('/product/<string:product_id>', methods=['DELETE'])
@token_required
def delete_product(token, product_id):
    return jsonify({"mensagem": f"Deletar produto {product_id}"})


# RF: O sistema deve permitira importacao de vendas atravez de um arquivo
@main_bp.route('/sales/upload', methods=['POST'])
def upload_sales():
    return jsonify({"menssagem": "Esta é a rota de upload do arquivo de vendas"})


 
@main_bp.route('/')
def index():
    return jsonify({"menssagem": "Bem vindo ao StyleSync!"})





