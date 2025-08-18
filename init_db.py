#!/usr/bin/env python3
"""
Script para inicializar o banco de dados no Render
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.extensions import db
from src.models.relationship import Relationship
from datetime import datetime

def init_database():
    with app.app_context():
        print("🗄️  Criando tabelas no banco de dados...")
        db.create_all()
        
        # Verifica se já existe um relacionamento
        relationship = Relationship.query.first()
        if not relationship:
            print("💕 Criando relacionamento padrão...")
            relationship = Relationship(
                start_date=datetime(2024, 5, 18, 12, 0, 0),  # 18 de maio de 2024 às 12:00
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

if __name__ == "__main__":
    init_database()
