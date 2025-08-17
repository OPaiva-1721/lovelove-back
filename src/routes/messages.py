from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.message import Message
from src.extensions import db

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages', methods=['GET'])
def get_messages():
    """Retorna todas as mensagens"""
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return jsonify([message.to_dict() for message in messages])

@messages_bp.route('/messages/simple', methods=['POST'])
def send_message_simple():
    """Rota simples para enviar mensagens (sem autenticação para facilitar testes)"""
    data = request.get_json()

    # Verifica se todos os dados necessários foram passados
    if not data or not data.get('sender_id') or not data.get('recipient_id') or not data.get('content'):
        return jsonify({'error': 'Dados faltando: sender_id, recipient_id e content são obrigatórios'}), 422

    # Cria a nova mensagem
    message = Message(
        sender_id=data['sender_id'],
        recipient_id=data['recipient_id'],
        content=data['content']
    )

    # Adiciona a mensagem ao banco de dados
    db.session.add(message)
    db.session.commit()

    return jsonify(message.to_dict()), 201

@messages_bp.route('/messages', methods=['POST'])
@jwt_required()
def send_message():
    data = request.get_json()
    user_id = get_jwt_identity()  # Obtém o ID do usuário logado

    # Verifica se todos os dados necessários foram passados
    if not data or not data.get('recipient_id') or not data.get('content'):
        return jsonify({'error': 'Dados faltando: recipient_id e content são obrigatórios'}), 422

    # Cria a nova mensagem
    message = Message(
        sender_id=user_id,  # Usa o ID do usuário logado
        recipient_id=data['recipient_id'],
        content=data['content']
    )

    # Adiciona a mensagem ao banco de dados
    db.session.add(message)
    db.session.commit()

    return jsonify(message.to_dict()), 201



@messages_bp.route('/messages/<int:with_user_id>', methods=['GET'])
@jwt_required()
def get_conversation(with_user_id):
    """Recupera a conversa entre o usuário logado e outro usuário"""
    user_id = get_jwt_identity()  # Obtém o ID do usuário logado
    page = request.args.get('page', 1, type=int)  # Paginação

    messages = Message.query.filter(
        ((Message.sender_id == user_id) & (Message.recipient_id == with_user_id)) |
        ((Message.sender_id == with_user_id) & (Message.recipient_id == user_id))
    ).order_by(Message.timestamp.asc()).paginate(page, per_page=20, error_out=False)  # Paginação com limite de 20 mensagens por página

    return jsonify([m.to_dict() for m in messages.items])

@messages_bp.route('/messages/<int:message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    """Deleta mensagem se for o remetente"""
    user_id = get_jwt_identity()
    message = Message.query.get_or_404(message_id)

    if message.sender_id != user_id:
        return jsonify({'error': 'Você só pode deletar suas próprias mensagens'}), 403

    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Mensagem deletada com sucesso'}), 200

@messages_bp.route('/messages/<int:message_id>/read', methods=['PUT'])
@jwt_required()
def mark_message_as_read(message_id):
    """Marca a mensagem como lida"""
    user_id = get_jwt_identity()
    message = Message.query.get_or_404(message_id)

    if message.recipient_id != user_id:
        return jsonify({'error': 'Você só pode marcar como lida mensagens recebidas'}), 403

    # Marcar a mensagem como lida
    message.read = True
    db.session.commit()
    return jsonify(message.to_dict())
