from src.extensions import db
from datetime import datetime

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.Text)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_featured = db.Column(db.Boolean, default=False)  # Para fotos em destaque na home
    
    def __repr__(self):
        return f'<Photo {self.filename}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'caption': self.caption,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'is_featured': self.is_featured
        }

