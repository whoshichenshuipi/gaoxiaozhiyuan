from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.feedback import Feedback
from app.extensions import db
from app.utils.response import success_response, error_response

feedback_bp = Blueprint('student_feedback', __name__)

@feedback_bp.route('/feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    fb = Feedback(
        user_id=user_id,
        type=data.get('type'),
        content=data.get('content'),
        screenshot_url=data.get('screenshot_url')
    )
    db.session.add(fb)
    db.session.commit()
    return success_response(msg="Feedback submitted")

@feedback_bp.route('/feedback', methods=['GET'])
@jwt_required()
def list_my_feedback():
    user_id = get_jwt_identity()
    fbs = Feedback.query.filter_by(user_id=user_id).order_by(Feedback.create_time.desc()).all()
    return success_response([{
        "id": f.id,
        "type": f.type,
        "content": f.content,
        "status": f.status,
        "reply": f.reply,
        "reply_time": f.reply_time.strftime("%Y-%m-%d %H:%M:%S") if f.reply_time else None,
        "create_time": f.create_time.strftime("%Y-%m-%d %H:%M:%S")
    } for f in fbs])
