from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from src.models.user import User
from src.extensions import db, bcrypt

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Verifica se os dados foram enviados corretamente
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Dados faltando'}), 400

    # Verifica se o nome de usuário já está registrado
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Nome de usuário já registrado'}), 400

    # Verifica se o email já está registrado
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já registrado'}), 400

    # Criação do novo usuário
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    # Criação do token JWT
    access_token = create_access_token(identity=new_user.id)

    return jsonify({'message': 'Usuário criado com sucesso!', 'access_token': access_token}), 201

# Rota de Login

@auth_bp.route('/login', methods=['POST'])  
def login():
    data = request.get_json()

    # Verifica se os dados foram enviados corretamente
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Dados faltando'}), 400

    # Verifica se o email existe
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Credenciais inválidas'}), 401

    # Criação do token JWT
    access_token = create_access_token(identity=user.id)

    return jsonify({'message': 'Login bem-sucedido', 'access_token': access_token}), 200