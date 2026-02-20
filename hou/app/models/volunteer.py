from datetime import datetime
from app.extensions import db

class VolunteerPlan(db.Model):
    __tablename__ = 'volunteer_plan'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('sys_user.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 备选库, 模拟方案
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'), nullable=False)
    priority = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    user = db.relationship('User', backref=db.backref('volunteer_plans', lazy=True))
    university = db.relationship('University')
    major = db.relationship('Major')
