# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class URL(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_id = db.Column(db.String(6), unique=True, nullable=False)
    
    def __init__(self, original_url, short_id):
        self.original_url = original_url
        self.short_id = short_id
