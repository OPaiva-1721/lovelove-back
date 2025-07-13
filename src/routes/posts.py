from flask import Blueprint, jsonify, request, current_app
from src.models.user import db
from src.models.post import Post
import os
from werkzeug.utils import secure_filename
from datetime import datetime

posts_bp = Blueprint('posts', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@posts_bp.route('/posts', methods=['GET'])
def get_posts():
    """Retorna todos os posts do feed"""
    posts = Post.query.order_by(Post.created_date.desc()).all()
    return jsonify([post.to_dict() for post in posts])

@posts_bp.route('/posts', methods=['POST'])
def create_post():
    """Cria novo post no feed"""
    data = request.get_json() if request.is_json else request.form
    
    if not data or not data.get('content'):
        return jsonify({'error': 'Conteúdo é obrigatório'}), 400
    
    post = Post(
        content=data['content'],
        author=data.get('author', 'Casal')
    )
    
    # Se tem imagem
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = str(int(datetime.now().timestamp()))
            filename = f"post_{timestamp}_{filename}"
            
            upload_folder = os.path.join(current_app.static_folder, 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            post.image_filename = filename
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify(post.to_dict()), 201

@posts_bp.route('/posts/<int:post_id>/like', methods=['PUT'])
def like_post(post_id):
    """Adiciona like ao post"""
    post = Post.query.get_or_404(post_id)
    post.likes += 1
    db.session.commit()
    return jsonify(post.to_dict())

@posts_bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Deleta um post"""
    post = Post.query.get_or_404(post_id)
    
    # Remove arquivo de imagem se existir
    if post.image_filename:
        file_path = os.path.join(current_app.static_folder, 'uploads', post.image_filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'message': 'Post deletado com sucesso'})

