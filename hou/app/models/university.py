from datetime import datetime
from app.extensions import db

class University(db.Model):
    __tablename__ = 'university'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, index=True)
    level = db.Column(db.String(64))  # 985, 211, 双高, 普通
    region = db.Column(db.String(64))
    intro = db.Column(db.Text)
    official_url = db.Column(db.String(255))
    auth_file_url = db.Column(db.String(255)) # 高校授权文件 PDF URL
    audit_status = db.Column(db.Integer, default=1) # 0: 待审, 1: 通过, -1: 驳回
    status = db.Column(db.Integer, default=1) # 1: active, 0: disabled

class Major(db.Model):
    __tablename__ = 'major'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, index=True)
    category = db.Column(db.String(64))
    discipline = db.Column(db.String(64))
    intro = db.Column(db.Text)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
    
    university = db.relationship('University', backref=db.backref('majors', lazy=True))

class AdmissionScore(db.Model):
    __tablename__ = 'admission_score'
    
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    province = db.Column(db.String(64), nullable=False)
    min_score = db.Column(db.Integer)
    min_rank = db.Column(db.Integer)
    avg_score = db.Column(db.Integer)
    plan_num = db.Column(db.Integer)
    status = db.Column(db.Integer, default=1)
    
    university = db.relationship('University')
    major = db.relationship('Major')
