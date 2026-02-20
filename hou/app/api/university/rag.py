from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.models.qa import KnowledgeBase
from app.extensions import db
from app.utils.response import success_response, error_response
from app.utils.auth import role_required

uni_rag_bp = Blueprint('university_rag_side', __name__)

@uni_rag_bp.route('/rag/upload', methods=['POST'])
@jwt_required()
@role_required('university')
def university_upload_rag():
    # 上传 RAG 文档申请
    data = request.get_json()
    doc = KnowledgeBase(
        university_id=1, # 桩代码
        doc_name=data.get('doc_name'),
        doc_url=data.get('doc_url'),
        status=0 # 待管理员审核
    )
    db.session.add(doc)
    db.session.commit()
    return success_response(msg="Document uploaded, pending admin audit")

@uni_rag_bp.route('/rag', methods=['GET'])
@jwt_required()
@role_required('university')
def list_uni_rag():
    docs = KnowledgeBase.query.filter_by(university_id=1).all()
    return success_response([{
        "id": d.id,
        "doc_name": d.doc_name,
        "status": d.status,
        "create_time": d.create_time.strftime("%Y-%m-%d %H:%M:%S")
    } for d in docs])
