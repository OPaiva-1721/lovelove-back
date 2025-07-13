from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.relationship import Relationship
from datetime import datetime, date

relationship_bp = Blueprint('relationship', __name__)

@relationship_bp.route('/relationship', methods=['GET'])
def get_relationship_info():
    """Retorna informações do relacionamento e contador de dias"""
    relationship = Relationship.query.first()
    
    if not relationship:
        relationship = Relationship(
            start_date=date(2024, 5, 18),
            partner1_name="Ele",
            partner2_name="Ela",
            anniversary_message="Nosso amor cresce a cada dia! ❤️"
        )
        db.session.add(relationship)
        db.session.commit()
    
    return jsonify({
        'relationship': relationship.to_dict(),
        'days_together': relationship.days_together()
    })

@relationship_bp.route('/relationship', methods=['PUT'])
def update_relationship():
    """Atualiza informações do relacionamento"""
    data = request.get_json()
    relationship = Relationship.query.first()
    
    if not relationship:
        return jsonify({'error': 'Relacionamento não encontrado'}), 404
    
    if 'partner1_name' in data:
        relationship.partner1_name = data['partner1_name']
    if 'partner2_name' in data:
        relationship.partner2_name = data['partner2_name']
    if 'anniversary_message' in data:
        relationship.anniversary_message = data['anniversary_message']
    
    db.session.commit()
    
    return jsonify({
        'relationship': relationship.to_dict(),
        'days_together': relationship.days_together()
    })

