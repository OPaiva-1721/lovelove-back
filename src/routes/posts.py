from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from src.models.post import Post
from src.models.comment import Comment
from src.extensions import db

posts_bp = Blueprint('posts', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    """Salva a imagem na pasta 'uploads' e retorna o caminho"""
    filename = secure_filename(file.filename)
    timestamp = str(int(datetime.now().timestamp()))
    filename = f"post_{timestamp}_{filename}"
    
    # Usando current_app.static_folder para obter o caminho correto
    upload_folder = os.path.join(current_app.static_folder, 'uploads')  # Usando current_app para acessar o diretório
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    
    return filename

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
        user_id=data.get('user_id', 1)  # Atribuindo um user_id padrão caso não seja passado
    )
    
    # Verifica e salva a imagem, se houver
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            post.image_filename = save_image(file)  # Usando a função save_image sem passar o app
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify(post.to_dict()), 201

@posts_bp.route('/posts/<int:post_id>/like', methods=['PUT'])
def like_post(post_id):
    """Adiciona like ao post"""
    post = Post.query.get_or_404(post_id)
    post.add_like()  # Método da classe Post para adicionar o like
    return jsonify(post.to_dict())

@posts_bp.route('/posts/<int:post_id>/comment', methods=['POST'])
def comment_on_post(post_id):
    """Adiciona um comentário a um post"""
    data = request.get_json()

    if not data or not data.get('content'):
        return jsonify({'error': 'Conteúdo do comentário é obrigatório'}), 400

    post = Post.query.get_or_404(post_id)
    
    # Cria e adiciona o comentário
    comment = Comment(content=data['content'], post_id=post_id, user_id=data.get('user_id', 1))  # Ajuste conforme seu modelo de Comment
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201

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
