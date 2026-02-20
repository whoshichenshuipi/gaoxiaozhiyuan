from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from app.models.qa import UniversityFAQ
from app.extensions import db
from app.utils.response import success_response, error_response
from app.utils.auth import role_required

uni_faq_bp = Blueprint('university_faq', __name__)

@uni_faq_bp.route('/faq', methods=['GET', 'POST'])
@jwt_required()
@role_required('university')
def manage_faq():
    uni_id = get_jwt().get('university_id')
    if request.method == 'POST':
        data = request.get_json()
        faq = UniversityFAQ(
            university_id=uni_id,
            question=data.get('question'),
            answer=data.get('answer'),
            sort_weight=data.get('sort_weight', 0)
        )
        db.session.add(faq)
        db.session.commit()
        return success_response(msg="FAQ added")
        
    faqs = UniversityFAQ.query.filter_by(university_id=uni_id).order_by(UniversityFAQ.sort_weight.desc()).all()
    return success_response([{
        "id": f.id,
        "question": f.question,
        "answer": f.answer,
        "sort_weight": f.sort_weight
    } for f in faqs])

@uni_faq_bp.route('/faq/<int:faq_id>', methods=['PUT', 'DELETE'])
@jwt_required()
@role_required('university')
def update_delete_faq(faq_id):
    uni_id = get_jwt().get('university_id')
    faq = UniversityFAQ.query.filter_by(id=faq_id, university_id=uni_id).first_or_404()
    
    if request.method == 'DELETE':
        db.session.delete(faq)
        db.session.commit()
        return success_response(msg="FAQ deleted")
        
    data = request.get_json()
    faq.question = data.get('question', faq.question)
    faq.answer = data.get('answer', faq.answer)
    faq.sort_weight = data.get('sort_weight', faq.sort_weight)
    db.session.commit()
    return success_response(msg="FAQ updated")
