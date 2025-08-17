from datetime import datetime
from src.extensions import db

class Relationship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)  # Alterado de Date para DateTime
    partner1_name = db.Column(db.String(100))
    partner2_name = db.Column(db.String(100))
    anniversary_message = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Relationship started {self.start_date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'partner1_name': self.partner1_name,
            'partner2_name': self.partner2_name,
            'anniversary_message': self.anniversary_message
        }
    
    def days_together(self):
        """Calcula quantos dias estão juntos"""
        if self.start_date:
            return (datetime.now() - self.start_date).days
        return 0
    
    def time_together_detailed(self):
        """Calcula o tempo detalhado que estão juntos (anos, meses, dias, horas, minutos, segundos)"""
        if not self.start_date:
            return {
                'years': 0,
                'months': 0,
                'days': 0,
                'hours': 0,
                'minutes': 0,
                'seconds': 0
            }
        
        now = datetime.now()
        diff = now - self.start_date
        
        # Cálculo de anos, meses e dias
        years = diff.days // 365
        remaining_days = diff.days % 365
        
        # Aproximação simples para meses (30 dias por mês)
        months = remaining_days // 30
        days = remaining_days % 30
        
        # Horas, minutos e segundos
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        seconds = diff.seconds % 60
        
        return {
            'years': years,
            'months': months,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        }