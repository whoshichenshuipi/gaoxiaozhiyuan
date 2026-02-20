from datetime import datetime
from app.extensions import db
import bcrypt

class User(db.Model):
    __tablename__ = 'sys_user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student, admin, university
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    status = db.Column(db.Integer, default=1)  # 1: active, 0: disabled, 2: pending_audit (for university)
    create_time = db.Column(db.DateTime, default=datetime.now)
    last_login_time = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Permission(db.Model):
    __tablename__ = 'sys_permission'
    
    id = db.Column(db.Integer, primary_key=True)
    permission_code = db.Column(db.String(64), unique=True, nullable=False)
    permission_name = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

class StudentProfile(db.Model):
    __tablename__ = 'student_profile'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('sys_user.id'), unique=True, nullable=False)
    score = db.Column(db.Integer)
    province = db.Column(db.String(32))
    subject_selection = db.Column(db.String(255)) # e.g., "physics,chemistry,biology"
    hobbies = db.Column(db.Text)
    region_preference = db.Column(db.String(255))
    specialty = db.Column(db.String(255))
    
    user = db.relationship('User', backref=db.backref('student_profile', uselist=False))
