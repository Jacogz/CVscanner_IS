from ...db import db
from ..models import documento
from werkzeug.utils import secure_filename

def obtener_documentos():
    documents = documento.Documento.query.all()
    # You may want to serialize your Documento objects properly here
    return {
        'status': 'exito',
        'documentos': [doc_to_dict(doc) for doc in documents],
        'msg': 'Documentos recuperados exitosamente.'
    }

def crear_documento(titulo, id_propietario, img, upload_folder):
    error = None
    if not titulo:
        error = 'Titulo requerido.'
    #elif not contenido:
    #    error = 'contenido requerido.'
    elif not id_propietario:
        error = 'ID de propietario requerido.'

    if error is not None:
        return {
            'status': 'fracaso',
            'msg': error
        }
    try:
        documento_nuevo = documento.Documento(
            titulo=titulo,
            id_propietario=id_propietario
        )
        db.session.add(documento_nuevo)
        db.session.flush()

        if img:
            nombre_archivo = secure_filename(img.filename)
            img_path = upload_folder + nombre_archivo
            imagen = documento.DocumentoImagen(
                documento_id=documento_nuevo.id,
                nombre_archivo=nombre_archivo,
                url=img_path
            )
            db.session.add(imagen)
            img.save(img_path)
        db.session.commit()
        return {
            'status': 'exito',
            'msg': f"Documento {titulo} creado exitosamente."
        }
    except Exception as e:
        db.session.rollback()
        return {
            'status': 'fracaso',
            'msg': f"Error al crear el documento: {str(e)}"
        }

def doc_to_dict(doc):
    # Customize this function to serialize your Documento objects as needed
    return {
        'id': doc.id,
        'titulo': doc.titulo,
        'texto_plano': doc.texto_plano,
        'fecha_creacion': doc.fecha_creacion.isoformat() if doc.fecha_creacion else None,
        'id_propietario': doc.id_propietario,
        'imagenes': [
            {
                'id': img.id,
                'nombre_archivo': img.nombre_archivo,
                'url': img.url,
                'fecha_subida': img.fecha_subida.isoformat() if img.fecha_subida else None
            } for img in doc.imagenes
        ],
        # Add more fields as needed
    }