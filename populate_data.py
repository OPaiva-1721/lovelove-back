#!/usr/bin/env python3
"""
Script para popular dados iniciais na rede social lovelove
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.extensions import db
from src.models.relationship import Relationship
from src.models.photo import Photo
from src.models.post import Post
from src.models.message import Message
from datetime import date, datetime
import shutil

def populate_initial_data():
    with app.app_context():
        # Limpa dados existentes
        db.drop_all()
        db.create_all()
        
        print("🏗️  Criando dados iniciais...")
        
        # 1. Cria usuários
        from src.models.user import User
        user1 = User(username="Ele", email="ele@lovelove.com")
        user1.set_password("123456")
        db.session.add(user1)
        
        user2 = User(username="Ela", email="ela@lovelove.com")
        user2.set_password("123456")
        db.session.add(user2)
        
        db.session.commit()
        
        # 2. Cria relacionamento
        relationship = Relationship(
            start_date=date(2024, 5, 18),
            partner1_name="Ele",
            partner2_name="Ela",
            anniversary_message="Nosso amor cresce a cada dia! ❤️"
        )
        db.session.add(relationship)
        db.session.commit()
        
        # 3. Cria pasta de uploads e copia fotos de exemplo
        uploads_dir = os.path.join(app.static_folder, 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Copia as fotos de exemplo que criamos
        assets_dir = os.path.join(os.path.dirname(__file__), "assets", "images")
        if not os.path.exists(assets_dir):
            assets_dir = "/home/ubuntu/rede_social_namorada/assets/images"
        
        for i, filename in enumerate(['casal_1.jpg', 'casal_2.jpg', 'casal_3.jpg'], 1):
            src = os.path.join(assets_dir, filename)
            dst = os.path.join(uploads_dir, filename)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                
                # Adiciona ao banco
                photo = Photo(
                    filename=filename,
                    caption=f"Momento especial {i} ❤️",
                    is_featured=True  # Todas em destaque na home
                )
                db.session.add(photo)
            else:
                print(f"⚠️  Arquivo {src} não encontrado, pulando...")
        
        # 4. Cria posts iniciais
        posts_data = [
            {
                "content": "Que dia lindo para estar com você! ☀️❤️",
                "user_id": 1,
                "image_filename": "casal_1.jpg"
            },
            {
                "content": "Nosso cafezinho da tarde sempre especial 🥰☕",
                "user_id": 1,
                "image_filename": "casal_2.jpg"
            },
            {
                "content": "Primavera chegou e nosso amor só floresce! 🌸💕",
                "user_id": 1,
                "image_filename": "casal_3.jpg"
            },
            {
                "content": "Cada dia ao seu lado é uma nova aventura! 🚀💖",
                "user_id": 1
            }
        ]
        
        for post_data in posts_data:
            post = Post(**post_data)
            db.session.add(post)
        
        # 5. Cria mensagens iniciais
        messages_data = [
            {"content": "Oi amor! Como foi seu dia? 😊", "sender_id": 1, "recipient_id": 2},
            {"content": "Oi meu bem! Foi ótimo, e o seu? ❤️", "sender_id": 2, "recipient_id": 1},
            {"content": "Também foi maravilhoso! Mal posso esperar para te ver 🥰", "sender_id": 1, "recipient_id": 2},
            {"content": "Eu também! Te amo muito ❤️", "sender_id": 2, "recipient_id": 1},
            {"content": "Te amo mais! 💕", "sender_id": 1, "recipient_id": 2}
        ]
        
        for msg_data in messages_data:
            message = Message(**msg_data)
            db.session.add(message)
        
        # Salva tudo
        db.session.commit()
        
        print("✅ Dados iniciais criados com sucesso!")
        print(f"📅 Relacionamento iniciado em: {relationship.start_date}")
        print(f"⏰ Dias juntos: {relationship.days_together()}")
        print(f"📸 Fotos criadas: {Photo.query.count()}")
        print(f"📝 Posts criados: {Post.query.count()}")
        print(f"💬 Mensagens criadas: {Message.query.count()}")

if __name__ == "__main__":
    populate_initial_data()

