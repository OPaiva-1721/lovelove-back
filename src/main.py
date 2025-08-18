import os
import sys
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from src.routes.user import user_bp
from src.routes.relationship import relationship_bp
from src.routes.photos import photos_bp
from src.routes.posts import posts_bp
from src.routes.messages import messages_bp
from src.routes.test import test_bp
from src.extensions import db, bcrypt, jwt
from src.routes.auth_bp import auth_bp

app = Flask(__name__)

# Carregando configurações do arquivo config.py
from config import Config
app.config.from_object(Config)

# Habilita CORS para comunicação com frontend
CORS(app, 
     origins=[
         "http://localhost:5173",  # Vite/React local
         "http://127.0.0.1:5173",  # Vite/React local (alternativo)
         "http://localhost:3000",  # React padrão
         "http://127.0.0.1:3000",  # React padrão (alternativo)
         "*"  # Permite todas as origens (fallback)
     ],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     supports_credentials=True)

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
        print(f"🔗 URI do banco: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
        
        # Força a criação de todas as tabelas
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")
        
        # Lista as tabelas criadas
        try:
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Tabelas disponíveis: {', '.join(tables)}")
        except Exception as e:
            print(f"⚠️  Não foi possível listar tabelas: {str(e)}")
        
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
        import traceback
        traceback.print_exc()
        # Continua mesmo com erro para não quebrar a aplicação

# Rota raiz para verificar se a API está funcionando
@app.route('/')
def home():
    return {
        'message': 'LoveLove API está funcionando! ❤️',
        'version': '1.0.0',
        'endpoints': {
            'relationship': '/api/relationship',
            'photos': '/api/photos/featured',
            'posts': '/api/posts',
            'messages': '/api/messages',
            'auth': '/api/auth'
        }
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
