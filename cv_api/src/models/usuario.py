from ...db import db

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    contrasena = db.Column(db.String(120), nullable=False)
    documentos = db.relationship('Documento', back_populates='propietario')
    
    def __repr__(self):
        return f'<Usuario {self.nombre_usuario}>'