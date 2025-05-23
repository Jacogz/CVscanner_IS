import functools
from flask import Blueprint, jsonify, flash, g, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import usuario
from ...db import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/registro', methods=['POST'])
def registro():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contrasena = request.form['contrasena']
        error = None

        if not nombre_usuario:
            error = 'Nombre de usuario requerido.'
        elif not contrasena:
            error = 'Contraseña requerida.'

        if error is None:
            try:
                
                db.session.add(usuario.Usuario(nombre_usuario=nombre_usuario, contrasena=contrasena))
                db.session.commit()
                return {
                    'status': 'exito',
                    'msg': f"Usuario {nombre_usuario} registrado exitosamente."
                }
            except Exception as e:
                db.session.rollback()
                return {
                    'status': 'fracaso',
                    'msg': f"Error al registrar el usuario: {str(e)}"
                    }
        else:
            return {
                'status': 'fracaso',
                'msg': error
            }

@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form('nombre_usuario')
        contrasena = request.form('contrasena')
        error = None
        
        if not nombre_usuario:
            error = 'Nombre de usuario requerido.'
        elif not contrasena:
            error = 'Contraseña requerida.'

        if error is None:
            try:
                usuario = usuario.Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
                
                if usuario is None:
                    error = 'Usuario no encontrado.'
                
                else:
                    if not contrasena == usuario.contrasena:
                        error = 'Contraseña incorrecta.'
                    else:
                        return {
                            'status': 'exito',
                            'msg': f"Usuario {nombre_usuario} logueado exitosamente."
                        }
            except Exception as e:
                return {
                    'status': 'fracaso',
                    'msg': f"Error al iniciar sesión: {str(e)}"
                }