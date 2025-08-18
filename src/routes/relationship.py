from flask import Blueprint, jsonify, request
from src.extensions import db
from src.models.relationship import Relationship
from datetime import datetime, date

relationship_bp = Blueprint('relationship', __name__)

@relationship_bp.route('/relationship', methods=['GET'])
def get_relationship_info():
    """Retorna informações do relacionamento e contador de dias"""
    try:
        relationship = Relationship.query.first()
        
        if not relationship:
            # Cria um relacionamento padrão se não existir
            relationship = Relationship(
                start_date=datetime(2024, 5, 18, 12, 0, 0),  # Usando datetime em vez de date
                partner1_name="Gabryel",
                partner2_name="Amabilly",
                anniversary_message="Nosso amor crescendo a cada dia! ❤️"
            )
            db.session.add(relationship)
            db.session.commit()
        
        return jsonify({
            'relationship': relationship.to_dict(),
            'days_together': relationship.days_together(),
            'time_together_detailed': relationship.time_together_detailed()
        })
    except Exception as e:
        print(f"Erro na rota /relationship: {str(e)}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@relationship_bp.route('/relationship', methods=['PUT'])
def update_relationship():
    """Atualiza informações do relacionamento"""
    try:
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
        
        # Alterando start_date para incluir hora, minuto e segundo
        if 'start_date' in data:
            try:
                # O formato deve ser "YYYY-MM-DDTHH:MM:SS" para incluir a hora
                relationship.start_date = datetime.strptime(data['start_date'], "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                return jsonify({'error': 'Formato de data inválido. Use o formato: YYYY-MM-DDTHH:MM:SS'}), 400
        
        db.session.commit()
        
        return jsonify({
            'relationship': relationship.to_dict(),
            'days_together': relationship.days_together(),
            'time_together_detailed': relationship.time_together_detailed()
        })
    except Exception as e:
        print(f"Erro na rota PUT /relationship: {str(e)}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500
