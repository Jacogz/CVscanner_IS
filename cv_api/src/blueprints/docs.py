from flask import Blueprint, request, current_app
from ..services import servicio_documentos, servicio_ocr

bp = Blueprint('docs', __name__)

@bp.route('/docs')
def get_docs():
    return servicio_documentos.obtener_documentos()

@bp.route('/crear', methods=['POST'])
def crear():
    if request.method == 'POST':
        titulo = request.form['titulo']
        id_propietario = request.form['id_propietario']
        img = request.files.get('imagen')

        return servicio_documentos.crear_documento(
            titulo=titulo,
            id_propietario=id_propietario,
            img=img,
            upload_folder=current_app.config['UPLOAD_FOLDER']
        )