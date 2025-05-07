from flask import Blueprint, jsonify, request, g
from werkzeug.exceptions import abort
from cv_api.db import get_db

bp = Blueprint('docs', __name__)

@bp.route('/docs')
def get_docs():
    db = get_db()
    documents = db.execute(
        'SELECT doc.id, title, content, created_at, owner_id, username'
        ' FROM document doc JOIN user ON doc.owner_id = user.id'
        ' ORDER BY created_at DESC'
    ).fetchall()
    return {
        'status': 'success',
        'documents': [dict(document) for document in documents],
        'message': 'Documents retrieved successfully.'
    }

@bp.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        owner_id = request.form['owner_id']
        
        error = None

        if not title:
            error = 'Title is required.'
        elif not content:
            error = 'Content is required.'
        elif not owner_id:
            error = 'Owner ID is required.'

        if error is not None:
            return {
                'status': 'failure',
                'message': error
            }
        else:
            db = get_db()
            db.execute(
                'INSERT INTO document (title, content, owner_id)'
                ' VALUES (?, ?, ?)',
                (title, content, owner_id)
            )
            db.commit()
            return {
                'status': 'success',
                'message': f"Document '{title}' created successfully."
            }