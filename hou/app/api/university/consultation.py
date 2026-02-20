from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.models.consultation import ConsultationMessage, LeaveMessage
from app.models.user import User
from app.extensions import db
from app.utils.response import success_response, error_response
from app.utils.auth import role_required

uni_msg_bp = Blueprint('university_consultation', __name__)

@uni_msg_bp.route('/consultation/sessions', methods=['GET'])
@jwt_required()
@role_required('university')
def list_uni_sessions():
    # 获取与本校有关的所有考生会话列表
    user_id = get_jwt_identity()
    # 简单逻辑：查询所有发给该账号的消息
    msgs = db.session.query(ConsultationMessage.sender_id).filter_by(receiver_id=user_id).distinct().all()
    sessions = []
    for (sid,) in msgs:
        user = User.query.get(sid)
        sessions.append({
            "user_id": sid,
            "username": user.username,
            "last_msg": "..."
        })
    return success_response(sessions)

@uni_msg_bp.route('/consultation/messages', methods=['GET'])
@jwt_required()
@role_required('university')
def list_uni_messages():
    user_id = get_jwt_identity()
    target_id = request.args.get('user_id')
    msgs = ConsultationMessage.query.filter(
        ((ConsultationMessage.sender_id == user_id) & (ConsultationMessage.receiver_id == target_id)) |
        ((ConsultationMessage.sender_id == target_id) & (ConsultationMessage.receiver_id == user_id))
    ).order_by(ConsultationMessage.send_time.asc()).all()
    
    return success_response([{
        "id": m.id,
        "sender_id": m.sender_id,
        "content": m.content,
        "time": m.send_time.strftime("%Y-%m-%d %H:%M:%S")
    } for m in msgs])

@uni_msg_bp.route('/consultation/messages', methods=['POST'])
@jwt_required()
@role_required('university')
def send_uni_message():
    user_id = get_jwt_identity()
    data = request.get_json()
    msg = ConsultationMessage(
        sender_id=user_id,
        receiver_id=data.get('receiver_id'),
        content=data.get('content')
    )
    db.session.add(msg)
    db.session.commit()
    return success_response(msg="Message sent")

@uni_msg_bp.route('/leave-messages', methods=['GET'])
@jwt_required()
@role_required('university')
def list_uni_leave_messages():
    uni_id = get_jwt().get('university_id')
    l_msgs = LeaveMessage.query.filter_by(university_id=uni_id).all()
    return success_response([{
        "id": m.id,
        "user": m.user.username if m.user else "Anonymous",
        "content": m.content,
        "reply": m.reply,
        "status": m.status,
        "create_time": m.create_time.strftime("%Y-%m-%d %H:%M:%S")
    } for m in l_msgs])

@uni_msg_bp.route('/leave-messages/<int:msg_id>/reply', methods=['PUT'])
@jwt_required()
@role_required('university')
def reply_leave_message(msg_id):
    data = request.get_json()
    msg = LeaveMessage.query.get_or_404(msg_id)
    msg.reply = data.get('reply')
    msg.status = 1
    db.session.commit()
    return success_response(msg="Replied")
