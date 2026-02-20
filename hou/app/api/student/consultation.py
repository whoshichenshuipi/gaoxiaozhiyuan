from flask import Blueprint, request, Response, stream_with_context
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.consultation import ConsultationMessage, LeaveMessage
from app.models.qa import QARecords
from app.extensions import db
from app.utils.response import success_response, error_response
from app.utils.auth import role_required
import time

msg_bp = Blueprint('student_consultation', __name__)

@msg_bp.route('/qa/general', methods=['POST'])
@jwt_required()
def general_qa():
    from app.utils.rag_engine import rag_engine
    data = request.get_json()
    question = data.get('question')
    university_id = data.get('university_id')
    
    start_time = time.time()
    answer, rag_used = rag_engine.answer_with_fallback(question, university_id)
    response_time = int((time.time() - start_time) * 1000)
    
    record = QARecords(
        user_id=get_jwt_identity(),
        university_id=university_id,
        question=question,
        answer=answer,
        rag_used=rag_used,
        response_time=response_time
    )
    db.session.add(record)
    db.session.commit()
    
    return success_response({"answer": answer, "rag_used": rag_used})

@msg_bp.route('/consultation/messages', methods=['GET'])
@jwt_required()
def list_messages():
    user_id = get_jwt_identity()
    messages = ConsultationMessage.query.filter(
        (ConsultationMessage.sender_id == user_id) | 
        (ConsultationMessage.receiver_id == user_id)
    ).order_by(ConsultationMessage.send_time.asc()).all()
    
    return success_response([{
        "id": m.id,
        "sender_id": m.sender_id,
        "content": m.content,
        "msg_type": m.msg_type,
        "send_time": m.send_time.strftime("%Y-%m-%d %H:%M:%S")
    } for m in messages])

@msg_bp.route('/consultation/messages', methods=['POST'])
@jwt_required()
def send_message():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    msg = ConsultationMessage(
        sender_id=user_id,
        receiver_id=data.get('receiver_id'), # 目标高校或管理员
        content=data.get('content'),
        msg_type=data.get('msg_type', 'text')
    )
    db.session.add(msg)
    db.session.commit()
    return success_response(msg="Message sent")

@msg_bp.route('/university/<int:uni_id>/leave-message', methods=['POST'])
@jwt_required()
def leave_university_message(uni_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    l_msg = LeaveMessage(
        user_id=user_id,
        university_id=uni_id,
        content=data.get('content')
    )
    db.session.add(l_msg)
    db.session.commit()
    return success_response(msg="Leave message submitted")
