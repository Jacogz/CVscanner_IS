from ...db import db

class Documento(db.Model):
    __tablename__ = 'documento'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    contenido_json = db.Column(db.JSON, nullable=False, default={})
    fecha_creacion = db.Column(db.DateTime, server_default=db.func.now())
    id_propietario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    imagenes = db.relationship('DocumentoImagen', back_populates='documento', cascade='all, delete-orphan')
    
    propietario = db.relationship('Usuario', back_populates='documentos')
    
    def __repr__(self):
        return f'<Documento {self.titulo}>'

class DocumentoImagen(db.Model):
    __tablename__ = 'documento_imagen'
    
    id = db.Column(db.Integer, primary_key=True)
    documento_id = db.Column(db.Integer, db.ForeignKey('documento.id'), nullable=False)
    nombre_archivo = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    fecha_subida = db.Column(db.DateTime, server_default=db.func.now())
    
    documento = db.relationship('Documento', back_populates='imagenes')
    
    def __repr__(self):
        return f'<DocumentoImagen {self.documento_id}>'