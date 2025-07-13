from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.message import Message

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages', methods=['GET'])
def get_messages():
    """Retorna todas as mensagens do chat"""
    messages = Message.query.order_by(Message.timestamp.asc()).all()
    return jsonify([message.to_dict() for message in messages])

@messages_bp.route('/messages', methods=['POST'])
def send_message():
    """Envia nova mensagem"""
    data = request.get_json()
    
    if not data or not data.get('content') or not data.get('sender'):
        return jsonify({'error': 'Conteúdo e remetente são obrigatórios'}), 400
    
    # Valida sender
    if data['sender'] not in ['ele', 'ela']:
        return jsonify({'error': 'Remetente deve ser "ele" ou "ela"'}), 400
    
    message = Message(
        content=data['content'],
        sender=data['sender']
    )
    
    db.session.add(message)
    db.session.commit()
    
    return jsonify(message.to_dict()), 201

@messages_bp.route('/messages/<int:message_id>/read', methods=['PUT'])
def mark_as_read(message_id):
    """Marca mensagem como lida"""
    message = Message.query.get_or_404(message_id)
    message.is_read = True
    db.session.commit()
    return jsonify(message.to_dict())

@messages_bp.route('/messages/unread-count', methods=['GET'])
def get_unread_count():
    """Retorna quantidade de mensagens não lidas"""
    sender = request.args.get('sender')
    if sender:
        count = Message.query.filter_by(sender=sender, is_read=False).count()
    else:
        count = Message.query.filter_by(is_read=False).count()
    
    return jsonify({'unread_count': count})

@messages_bp.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    """Deleta uma mensagem"""
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Mensagem deletada com sucesso'})

