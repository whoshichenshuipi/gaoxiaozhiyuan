from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import StudentProfile, User
from app.extensions import db
from app.utils.response import success_response, error_response
from app.utils.auth import role_required

student_bp = Blueprint('student', __name__)

@student_bp.route('/profile', methods=['GET'])
@jwt_required()
@role_required('student')
def get_profile():
    user_id = get_jwt_identity()
    profile = StudentProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return error_response(msg="Profile not found")
        
    return success_response({
        "score": profile.score,
        "province": profile.province,
        "subject_selection": profile.subject_selection,
        "hobbies": profile.hobbies,
        "region_preference": profile.region_preference,
        "specialty": profile.specialty
    })

@student_bp.route('/profile', methods=['POST'])
@jwt_required()
@role_required('student')
def update_profile():
    user_id = get_jwt_identity()
    profile = StudentProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = StudentProfile(user_id=user_id)
        db.session.add(profile)
        
    data = request.get_json()
    profile.score = data.get('score', profile.score)
    profile.province = data.get('province', profile.province)
    profile.subject_selection = data.get('subject_selection', profile.subject_selection)
    profile.hobbies = data.get('hobbies', profile.hobbies)
    profile.region_preference = data.get('region_preference', profile.region_preference)
    profile.specialty = data.get('specialty', profile.specialty)
    
    db.session.commit()
    return success_response(msg="Profile updated")
