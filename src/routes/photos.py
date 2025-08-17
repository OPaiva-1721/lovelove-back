from flask import Blueprint, jsonify, request, current_app
from src.models.photo import Photo
from src.extensions import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime

photos_bp = Blueprint('photos', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rota para retornar todas as fotos
@photos_bp.route('/photos', methods=['GET'])
def get_all_photos():
    """Retorna todas as fotos"""
    photos = Photo.query.order_by(Photo.upload_date.desc()).all()
    return jsonify([photo.to_dict() for photo in photos])

# Rota para retornar fotos em destaque
@photos_bp.route('/photos/featured', methods=['GET'])
def get_featured_photos():
    """Retorna fotos em destaque para a página inicial"""
    photos = Photo.query.filter_by(is_featured=True).order_by(Photo.upload_date.desc()).all()
    return jsonify([photo.to_dict() for photo in photos])

# Rota para upload de fotos
@photos_bp.route('/photos', methods=['POST'])
def upload_photo():
    """Upload de nova foto"""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Garante nome único
        timestamp = str(int(datetime.now().timestamp()))
        filename = f"{timestamp}_{filename}"
        
        upload_folder = os.path.join(current_app.static_folder, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Salva no banco
        photo = Photo(
            filename=filename,
            caption=request.form.get('caption', ''),
            is_featured=request.form.get('is_featured', 'false').lower() == 'true'
        )
        db.session.add(photo)
        db.session.commit()
        
        return jsonify(photo.to_dict()), 201
    
    return jsonify({'error': 'Tipo de arquivo não permitido'}), 400

# Alterna o status de "foto em destaque"
@photos_bp.route('/photos/<int:photo_id>/toggle-featured', methods=['PUT'])
def toggle_featured(photo_id):
    """Alterna status de foto em destaque"""
    photo = Photo.query.get_or_404(photo_id)
    photo.is_featured = not photo.is_featured
    db.session.commit()
    return jsonify(photo.to_dict())
