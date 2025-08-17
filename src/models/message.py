from src.extensions import db
from datetime import datetime

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)  # Campo para marcar se foi lida

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')

    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')

    def __repr__(self):
        return f'<Message {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'read': self.read,
            'sender_id': self.sender_id,
            'sender_username': self.sender.username if self.sender else None,
            'recipient_id': self.recipient_id,
            'recipient_username': self.recipient.username if self.recipient else None
        }
