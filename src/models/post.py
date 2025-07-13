from src.models.user import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255))  # Opcional
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    author = db.Column(db.String(100), default='Casal')  # Sem login, mas pode identificar quem postou
    
    def __repr__(self):
        return f'<Post {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'image_filename': self.image_filename,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'likes': self.likes,
            'author': self.author
        }

