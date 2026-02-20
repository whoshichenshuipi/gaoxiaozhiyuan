from datetime import datetime
from app.extensions import db

class OperationLog(db.Model):
    __tablename__ = 'sys_operation_log'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('sys_user.id'))
    operation_type = db.Column(db.String(50))
    content = db.Column(db.Text)
    ip = db.Column(db.String(45))
    operation_time = db.Column(db.DateTime, default=datetime.now)
    
    user = db.relationship('User')

class StudentSource(db.Model):
    __tablename__ = 'student_source'
    
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('sys_user.id'), nullable=False)
    volunteer_type = db.Column(db.String(20)) # 备选库 / 模拟方案
    score = db.Column(db.Integer)
    province = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    university = db.relationship('University')
    user = db.relationship('User')
