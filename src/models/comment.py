from src.extensions import db
from datetime import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    post = db.relationship('Post', backref=db.backref('related_comments', lazy=True))  # Referência ao backref alterado

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='comments')

    def __repr__(self):
        return f'<Comment {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None
        }
