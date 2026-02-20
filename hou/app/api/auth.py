from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from app.models.user import User, StudentProfile
from app.extensions import db
from app.utils.response import success_response, error_response
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        if user.status == 0:
            return error_response(code=403, msg="Account disabled")
        if user.status == 2:
            return error_response(code=403, msg="University account pending audit")
            
        access_token = create_access_token(
            identity=user.id, 
            additional_claims={
                "role": user.role,
                "university_id": user.university_id
            }
        )
        refresh_token = create_refresh_token(identity=user.id)
        
        user.last_login_time = datetime.now()
        db.session.commit()
        
        return success_response({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
        })
    
    return error_response(code=401, msg="Invalid username or password")

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'student') # student, university
    
    if User.query.filter_by(username=username).first():
        return error_response(msg="Username already exists")
        
    user = User(username=username, role=role)
    user.set_password(password)
    
    if role == 'university':
        university_name = data.get('university_name')
        from app.models.university import University
        school = University.query.filter_by(name=university_name).first()
        if not school:
            return error_response(msg="University not found in our database")
        user.university_id = school.id
        user.status = 2 # Pending audit
    
    db.session.add(user)
    db.session.flush() # Get user id
    
    if role == 'student':
        profile = StudentProfile(user_id=user.id)
        db.session.add(profile)
        
    db.session.commit()
    
    return success_response(msg="Registration successful" + (" (Pending audit for university)" if role == 'university' else ""))

@auth_bp.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    user = User.query.get(identity)
    access_token = create_access_token(
        identity=identity, 
        additional_claims={
            "role": user.role,
            "university_id": user.university_id
        }
    )
    return success_response({"access_token": access_token})
