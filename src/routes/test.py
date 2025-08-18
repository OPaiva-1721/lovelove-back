from flask import Blueprint, jsonify

test_bp = Blueprint('test', __name__)

@test_bp.route('/test', methods=['GET'])
def test():
    """Rota de teste para verificar se o backend está funcionando"""
    return jsonify({
        'status': 'success',
        'message': 'Backend está funcionando!',
        'timestamp': '2024-08-18'
    })
