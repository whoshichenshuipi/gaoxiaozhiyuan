from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from app.utils.response import error_response

def role_required(*roles):
    """
    角色权限校验装饰器
    用法: @role_required('admin', 'university')
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('role') not in roles:
                return error_response(code=403, msg="Permission denied: Insufficient role")
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

def permission_required(permission_code):
    """
    具体操作权限校验装饰器（预留）
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            permissions = claims.get('permissions', [])
            if permission_code not in permissions and claims.get('role') != 'admin':
                return error_response(code=403, msg=f"Permission denied: Missing {permission_code}")
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
