from flask import Blueprint, request, current_app
from ..services import servicio_documentos, servicio_ocr

bp = Blueprint('docs', __name__)

@bp.route('/docs')
def get_docs():
    return servicio_documentos.obtener_documentos()

@bp.route('/create', methods=['POST'])
def create():
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
        
@bp.route('/extraer_json/<int:documento_id>')
def extraer_json(documento_id):
    
    return servicio_ocr.extraer_json()

@bp.route('/docs/<int:documento_id>', methods=['GET'])
def get_doc_detail(documento_id):
    return servicio_documentos.obtener_documento_por_id(documento_id)

@bp.route('/docs/json/<int:documento_id>', methods=['GET'])
def get_doc_json(documento_id):
    resultado = servicio_documentos.obtener_doc_json(documento_id)
    #print("DEBUG get_doc_json: ", resultado)
    return resultado['documento']

@bp.route('/docs/<int:documento_id>', methods=['PUT', 'PATCH'])
def update_doc(documento_id):
    data = request.form
    titulo = data.get('titulo')
    contenido_json = data.get('contenido_json')
    return servicio_documentos.actualizar_documento(documento_id, titulo=titulo, contenido_json=contenido_json)

@bp.route('/docs/<int:documento_id>', methods=['DELETE'])
def delete_doc(documento_id):
    return servicio_documentos.eliminar_documento(documento_id)