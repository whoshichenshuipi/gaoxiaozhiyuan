from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.university import University
from app.models.user import User
from app.extensions import db
from app.utils.response import success_response, error_response
from app.utils.auth import role_required

uni_info_bp = Blueprint('university_info_side', __name__)

@uni_info_bp.route('/register-info', methods=['POST'])
@jwt_required()
@role_required('university')
def update_university_registration_details():
    # 完善详细信息申请
    data = request.get_json()
    from flask_jwt_extended import get_jwt
    claims = get_jwt()
    uni_id = claims.get('university_id')
    
    uni = University.query.get(uni_id)
    if not uni:
        return error_response(msg="University record not found")
        
    uni.intro = data.get('intro', uni.intro)
    uni.official_url = data.get('official_url', uni.official_url)
    uni.audit_status = 0 # Re-submit for audit if details change majorly? Or just update.
    
    db.session.commit()
    return success_response(msg="Details updated and submitted for review")

@uni_info_bp.route('/info', methods=['GET'])
@jwt_required()
@role_required('university')
def get_own_university_info():
    from flask_jwt_extended import get_jwt
    claims = get_jwt()
    uni_id = claims.get('university_id')
    
    if not uni_id:
        return error_response(msg="No university associated with this account")
        
    uni = University.query.get(uni_id)
    if not uni:
        return error_response(msg="University not found")
    
    return success_response({
        "id": uni.id,
        "name": uni.name,
        "region": uni.region,
        "intro": uni.intro,
        "official_url": uni.official_url,
        "level": uni.level,
        "audit_status": uni.audit_status
    })

@uni_info_bp.route('/info', methods=['PUT'])
@jwt_required()
@role_required('university')
def update_own_university_info():
    data = request.get_json()
    from flask_jwt_extended import get_jwt
    claims = get_jwt()
    uni_id = claims.get('university_id')
    
    uni = University.query.get(uni_id)
    if not uni:
        return error_response(msg="University not found")
    
    uni.intro = data.get('intro', uni.intro)
    uni.official_url = data.get('official_url', uni.official_url)
    # 允许修改简介等非敏感信息
    db.session.commit()
    return success_response(msg="Info updated")

@uni_info_bp.route('/info/upload-image', methods=['POST'])
@jwt_required()
@role_required('university')
def upload_university_image():
    # 上传逻辑可以复用 app/api/common.py 中的逻辑
    # 这里仅作为占位，实际联调时对接
    return success_response(data={"url": "http://cdn.example.com/uni_image.jpg"}, msg="Image uploaded")
