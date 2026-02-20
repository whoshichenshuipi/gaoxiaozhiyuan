from flask import Blueprint, request
import psutil
from flask_jwt_extended import jwt_required
from app.models.system import OperationLog
from app.utils.response import success_response
from app.utils.auth import role_required

admin_sys_bp = Blueprint('admin_system', __name__)

@admin_sys_bp.route('/system/status', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_system_status():
    status = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total": psutil.virtual_memory().total,
            "used": psutil.virtual_memory().used,
            "percent": psutil.virtual_memory().percent
        },
        "disk": {
            "percent": psutil.disk_usage('/').percent
        }
    }
    return success_response(status)

@admin_sys_bp.route('/logs', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_logs():
    user_id = request.args.get('user_id', type=int)
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 20, type=int)
    
    query = OperationLog.query
    if user_id:
        query = query.filter_by(user_id=user_id)
        
    pagination = query.order_by(OperationLog.operation_time.desc()).paginate(page=page, per_page=page_size)
    
    return success_response({
        "list": [{
            "id": l.id,
            "user": l.user.username if l.user else "System",
            "type": l.operation_type,
            "content": l.content,
            "ip": l.ip,
            "time": l.operation_time.strftime("%Y-%m-%d %H:%M:%S")
        } for l in pagination.items],
        "total": pagination.total
    })
from app.models.feedback import Feedback
from datetime import datetime

@admin_sys_bp.route('/feedbacks', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_feedbacks():
    status = request.args.get('status', type=int)
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    
    query = Feedback.query
    if status is not None:
        query = query.filter_by(status=status)
        
    pagination = query.order_by(Feedback.create_time.desc()).paginate(page=page, per_page=page_size)
    
    return success_response({
        "list": [{
            "id": f.id,
            "type": f.type,
            "content": f.content,
            "status": f.status,
            "user": f.user.username if f.user else "Unknown",
            "reply": f.reply,
            "create_time": f.create_time.strftime("%Y-%m-%d %H:%M:%S")
        } for f in pagination.items],
        "total": pagination.total
    })

@admin_sys_bp.route('/feedbacks/<int:fb_id>/reply', methods=['POST'])
@jwt_required()
@role_required('admin')
def reply_feedback(fb_id):
    data = request.get_json()
    reply = data.get('reply')
    
    fb = Feedback.query.get_or_404(fb_id)
    fb.reply = reply
    fb.status = 1
    fb.reply_time = datetime.now()
    db.session.commit()
    
    return success_response(msg="Reply sent successfully")

from app.models.community import CommunityPost

@admin_sys_bp.route('/posts', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_all_posts():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    
    pagination = CommunityPost.query.order_by(CommunityPost.create_time.desc()).paginate(page=page, per_page=page_size)
    
    return success_response({
        "list": [{
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "author": p.user.username,
            "is_top": p.top_flag == 1,
            "time": p.create_time.strftime("%Y-%m-%d %H:%M:%S")
        } for p in pagination.items],
        "total": pagination.total
    })

@admin_sys_bp.route('/posts/<int:post_id>/top', methods=['PUT'])
@jwt_required()
@role_required('admin')
def toggle_post_top(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    post.top_flag = 1 if post.top_flag == 0 else 0
    db.session.commit()
    return success_response(msg="Post top status updated")

@admin_sys_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_post(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return success_response(msg="Post deleted")
