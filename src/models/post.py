from src.extensions import db
from datetime import datetime
from src.models.comment import Comment  # Importando o modelo Comment

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    image_filename = db.Column(db.String(255), nullable=True)
    likes = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", backref="posts")

    # Alterando o backref para evitar o conflito
    comments = db.relationship('Comment', backref='related_post', lazy=True)  # Mudamos o nome do backref para 'related_post'

    def __repr__(self):
        return f'<Post {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'image_filename': self.image_filename,
            'likes': self.likes,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'comments': [comment.to_dict() for comment in self.comments]  # Inclui os comentários
        }

    def add_like(self):
        """Adiciona uma curtida ao post"""
        self.likes += 1
        db.session.commit()

    def add_comment(self, content, user_id):
        """Adiciona um comentário ao post"""
        comment = Comment(content=content, post_id=self.id, user_id=user_id)
        db.session.add(comment)
        db.session.commit()
