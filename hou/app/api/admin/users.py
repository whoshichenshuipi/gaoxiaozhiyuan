from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.models.user import User
from app.extensions import db
from app.utils.response import success_response, error_response
from app.utils.auth import role_required

admin_user_bp = Blueprint('admin_user', __name__)

@admin_user_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_users():
    role = request.args.get('role')
    status = request.args.get('status', type=int)
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 20, type=int)
    
    query = User.query
    if role:
        query = query.filter_by(role=role)
    if status is not None:
        query = query.filter_by(status=status)
        
    pagination = query.order_by(User.create_time.desc()).paginate(page=page, per_page=page_size)
    
    return success_response({
        "list": [{
            "id": u.id,
            "username": u.username,
            "role": u.role,
            "status": u.status,
            "create_time": u.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": u.last_login_time.strftime("%Y-%m-%d %H:%M:%S") if u.last_login_time else None
        } for u in pagination.items],
        "total": pagination.total
    })

@admin_user_bp.route('/users/<int:user_id>/status', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_user_status(user_id):
    data = request.get_json()
    status = data.get('status') # 1: enabled, 0: disabled, 2: audit_pass (for uni)
    
    user = User.query.get_or_404(user_id)
    user.status = status
    db.session.commit()
    
    return success_response(msg="User status updated")

@admin_user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        return error_response(msg="Cannot delete admin user")
        
    db.session.delete(user)
    db.session.commit()
    return success_response(msg="User deleted")
