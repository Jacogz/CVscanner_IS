import functools
from flask import Blueprint, jsonify, flash, g, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from cv_api.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
                return {
                    'status': 'success',
                    'message': f"User {username} registered successfully."
                }
            except db.IntegrityError:
                return {
                    'status': 'failure',
                    'message': f"User {username} is already registered."
                    }
        else:
            return {
                'status': 'failure',
                'message': error
            }

@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            return {
                'status': 'success',
                'message': f"User {username} logged in successfully."
            }
        else:
            return {
                'status': 'failure',
                'message': error
            }

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))