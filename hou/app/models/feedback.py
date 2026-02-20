from datetime import datetime
from app.extensions import db

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('sys_user.id'), nullable=False)
    type = db.Column(db.String(50))  # 数据异常, 功能建议, 其他
    content = db.Column(db.Text, nullable=False)
    screenshot_url = db.Column(db.String(255))
    feedback_source = db.Column(db.String(20), default='student') # student, university
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    status = db.Column(db.Integer, default=0)  # 0: pending, 1: processed
    reply = db.Column(db.Text)
    reply_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    user = db.relationship('User')
