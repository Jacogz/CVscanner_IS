from ...db import db
from ..models import documento as doc
import pytesseract
from PIL import Image
from dotenv import load_dotenv
import os
from openai import OpenAI

def extraer_texto(img):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    if img:
        ruta_imagen = img.url
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
        return {
            'status': 'exito',
            'json_convertido': respuesta,
            'msg': 'Texto convertido a JSON exitosamente.'
        }
    except Exception as e:
        return {
            'status': 'fracaso',
            'msg': f'Error al convertir el texto a JSON: {str(e)}'
        }

def extraer_json(img):
    if not img:
        return {
            'status': 'fracaso',
            'msg': 'No se encontraron imágenes para extraer texto.'
        }
        
    resultado = extraer_texto(img)
    if resultado['status'] == 'exito':
        #print(resultado['texto_extraido'])
        json = texto_a_json(resultado['texto_extraido'])['json_convertido']
        return json
    else:
        return {
            'status': 'fracaso',
            'msg': 'No se pudo extraer texto para convertir a JSON.'
        }