from ...db import db
from ..models import documento as doc
import pytesseract
from PIL import Image
from dotenv import load_dotenv
import os
from openai import OpenAI

def extraer_texto():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    id_documento = 4
    documento = doc.Documento.query.get(id_documento)
    imagenes = documento.imagenes
    ultima_imagen = imagenes[-1] if imagenes else None
    if ultima_imagen:
        ruta_imagen = ultima_imagen.url
        texto_extraido = pytesseract.image_to_string(Image.open(ruta_imagen), config='--psm 6 -l spa')
        return {
            'status': 'exito',
            'texto_extraido': texto_extraido,
            'msg': 'Texto extraído exitosamente.'
        }
    else:
        return {
            'status': 'fracaso',
            'msg': 'No se encontraron imágenes para extraer texto.'
        }

def texto_a_json(texto):
    load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../api_keys.env')))
    client = OpenAI(api_key=os.environ.get('openai_apikey'))
    

    def get_completion(prompt, model="gpt-3.5-turbo"):
            msg = [{"role": "user", "content": prompt}]
            response = client.chat.completions.create(
                model=model,
                messages=msg,
                temperature=0,
            )
            return response.choices[0].message.content.strip()
    
    instruccion = (
        "Procesa el siguiente texto extraído de un CV y devuélvelo en formato JSON usando la estructura estandarizada. Corrige errores de ortografía y omite información inexistente. \n"
        "El JSON debe tener la siguiente estructura: \n"
        "{\n"
        '"nombre_completo": "",\n'
        '"contacto": {"direccion": "","telefono": "","email": "","linkedin": "" },\n'
        '"resumen_profesional": "",\n'
        '"experiencia_laboral": [{"puesto": "","empresa": "","ubicacion": "","fecha_inicio": "","fecha_fin": "","responsabilidades": [],"logros": [] }],\n'
        '"educacion": [{"titulo": "","institucion": "","ubicacion": "","fecha_inicio": "","fecha_fin": "" }],\n'
        '"habilidades": {"tecnicas": [],"blandas": [] },\n'
        '"certificaciones": [{"nombre": "","institucion": "","fecha": ""}],\n'
        '"idiomas": [{"idioma": "","nivel": "" }]\n'
        "}\n\n"
        
        "Texto extraído: \n"
        f"{texto}\n\n"
        "Por favor, devuelve el JSON sin ningún comentario adicional ni texto extra."
    )
    try:
        respuesta = get_completion(instruccion)
        return respuesta
    except Exception as e:
        return {
            'status': 'fracaso',
            'msg': f'Error al convertir el texto a JSON: {str(e)}'
        }

def extraer_json():
    texto = extraer_texto()['texto_extraido']
    if texto:
        return texto_a_json(texto)
    else:
        return {
            'status': 'fracaso',
            'msg': 'No se pudo extraer texto para convertir a JSON.'
        }