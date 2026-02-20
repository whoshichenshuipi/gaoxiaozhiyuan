from datetime import datetime
from app.extensions import db

class News(db.Model):
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50))  # 政策, 技巧, 公告
    publisher_type = db.Column(db.String(20), default='admin') # admin, university
    create_time = db.Column(db.DateTime, default=datetime.now)
    top_flag = db.Column(db.Boolean, default=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('sys_user.id'))
    status = db.Column(db.Integer, default=1)
    
    publisher = db.relationship('User')
