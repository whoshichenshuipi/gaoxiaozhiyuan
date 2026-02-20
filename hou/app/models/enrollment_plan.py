from datetime import datetime
from app.extensions import db

class EnrollmentPlan(db.Model):
    __tablename__ = 'enrollment_plan'
    
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    province = db.Column(db.String(64), nullable=False)
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'), nullable=False)
    plan_num = db.Column(db.Integer, nullable=False)
    requirement = db.Column(db.Text) # 选科要求
    status = db.Column(db.Integer, default=0) # 0: 待审核, 1: 已发布
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    university = db.relationship('University')
    major = db.relationship('Major')
