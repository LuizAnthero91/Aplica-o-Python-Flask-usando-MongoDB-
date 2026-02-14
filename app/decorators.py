from functools import wraps
from flask import request, jsonify, current_app, g
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token não enviado.'}), 401

        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({'error': 'Token mal formado.'}), 401

        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            g.user = data  # <-- AQUI

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado.'}), 401

        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido.'}), 401

        return f(*args, **kwargs)

    return decorated

