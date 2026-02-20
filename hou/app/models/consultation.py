from datetime import datetime
from app.extensions import db

class ConsultationMessage(db.Model):
    __tablename__ = 'consultation_message'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('sys_user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('sys_user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    msg_type = db.Column(db.String(20), default='text')  # text, image
    send_time = db.Column(db.DateTime, default=datetime.now)
    read_flag = db.Column(db.Boolean, default=False)
    
    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])

class LeaveMessage(db.Model):
    __tablename__ = 'leave_message'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('sys_user.id'), nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    reply = db.Column(db.Text)
    reply_time = db.Column(db.DateTime)
    status = db.Column(db.Integer, default=0)  # 0: unreplied, 1: replied
    
    user = db.relationship('User')
    university = db.relationship('University')
