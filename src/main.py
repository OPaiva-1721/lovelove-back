import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from src.routes.user import user_bp
from src.routes.relationship import relationship_bp
from src.routes.photos import photos_bp
from src.routes.posts import posts_bp
from src.routes.messages import messages_bp
from src.routes.test import test_bp
from src.extensions import db, bcrypt, jwt
from src.routes.auth_bp import auth_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Carregando configurações do arquivo config.py
from config import Config
app.config.from_object(Config)

# Habilita CORS para comunicação com frontend
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

# Configuração do banco de dados e criptografia
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

# Registra o blueprint de autenticação
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Registra todas as rotas
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(relationship_bp, url_prefix='/api')
app.register_blueprint(photos_bp, url_prefix='/api')
app.register_blueprint(posts_bp, url_prefix='/api')
app.register_blueprint(messages_bp, url_prefix='/api')
app.register_blueprint(test_bp, url_prefix='/api')

# Importa todos os modelos para criar as tabelas
from src.models.photo import Photo
from src.models.post import Post
from src.models.message import Message
from src.models.relationship import Relationship

# Criação das tabelas no banco de dados
with app.app_context():
    try:
        print("🗄️  Criando tabelas no banco de dados...")
        db.create_all()
        
        # Verifica se já existe um relacionamento
        from src.models.relationship import Relationship
        relationship = Relationship.query.first()
        if not relationship:
            print("💕 Criando relacionamento padrão...")
            relationship = Relationship(
                start_date=datetime(2024, 5, 18, 12, 0, 0),
                partner1_name="Gabryel",
                partner2_name="Amabilly",
                anniversary_message="Nosso amor crescendo a cada dia! ❤️"
            )
            db.session.add(relationship)
            db.session.commit()
            print("✅ Relacionamento criado com sucesso!")
        else:
            print("✅ Relacionamento já existe!")
            
        print("🎉 Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"⚠️  Erro ao inicializar banco: {str(e)}")
        # Continua mesmo com erro para não quebrar a aplicação

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
