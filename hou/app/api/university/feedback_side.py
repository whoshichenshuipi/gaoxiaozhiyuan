from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.models.feedback import Feedback
from app.extensions import db
from app.utils.response import success_response, error_response
from app.utils.auth import role_required

uni_feedback_bp = Blueprint('university_feedback_side', __name__)

@uni_feedback_bp.route('/feedback-to-admin', methods=['POST'])
@jwt_required()
@role_required('university')
def feedback_to_admin():
    user_id = get_jwt_identity()
    uni_id = get_jwt().get('university_id')
    data = request.get_json()
    
    fb = Feedback(
        user_id=user_id,
        university_id=uni_id,
        type=data.get('type'),
        content=data.get('content'),
        screenshot_url=data.get('attachment_url'), # Map to model field
        feedback_source='university'
    )
    db.session.add(fb)
    db.session.commit()
    return success_response(msg="Feedback submitted to admin")

@uni_feedback_bp.route('/feedback/my', methods=['GET'])
@jwt_required()
@role_required('university')
def list_my_feedback():
    user_id = get_jwt_identity()
    feedbacks = Feedback.query.filter_by(user_id=user_id).all()
    return success_response([{
        "id": f.id,
        "type": f.type,
        "content": f.content,
        "status": f.status,
        "reply": f.reply,
        "create_time": f.create_time.strftime("%Y-%m-%d %H:%M:%S")
    } for f in feedbacks])
