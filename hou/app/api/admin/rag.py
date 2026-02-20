from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.models.qa import KnowledgeBase, QAPromptTemplate
from app.extensions import db
from app.utils.response import success_response, error_response
from app.utils.auth import role_required

admin_rag_bp = Blueprint('admin_rag', __name__)

@admin_rag_bp.route('/rag/audit', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_pending_rag():
    docs = KnowledgeBase.query.filter_by(status=0).all()
    return success_response([{
        "id": d.id,
        "uni_name": d.university.name if d.university else "Universal",
        "doc_name": d.doc_name,
        "doc_url": d.doc_url,
        "create_time": d.create_time.strftime("%Y-%m-%d %H:%M:%S")
    } for d in docs])

@admin_rag_bp.route('/rag/audit/<int:doc_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def audit_rag(doc_id):
    data = request.get_json()
    action = data.get('action') # approve, reject
    
    doc = KnowledgeBase.query.get_or_404(doc_id)
    if action == 'approve':
        doc.status = 1
        # TODO: Trigger RAG ingestion pipeline (chunking + vectorization)
    else:
        doc.status = -1 # Rejected
        
    db.session.commit()
    return success_response(msg=f"Document {action}ed")

@admin_rag_bp.route('/qa/template', methods=['GET', 'POST'])
@jwt_required()
@role_required('admin')
def manage_templates():
    if request.method == 'POST':
        data = request.get_json()
        tmpl = QAPromptTemplate(
            template_type=data.get('type'),
            template_content=data.get('content'),
            variables=data.get('variables'),
            is_default=data.get('is_default', False)
        )
        if tmpl.is_default:
            QAPromptTemplate.query.filter_by(template_type=tmpl.template_type).update({"is_default": False})
        db.session.add(tmpl)
        db.session.commit()
        return success_response(msg="Template saved")
    
    tmpls = QAPromptTemplate.query.all()
    return success_response([{
        "id": t.id,
        "type": t.template_type,
        "content": t.template_content,
        "variables": t.variables,
        "is_default": t.is_default
    } for t in tmpls])
