from datetime import datetime
from app.extensions import db

class CommunityPost(db.Model):
    __tablename__ = 'community_post'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('sys_user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    like_num = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=1)  # 1: normal, 0: deleted/hidden
    top_flag = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User')

class CommunityComment(db.Model):
    __tablename__ = 'community_comment'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('community_post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('sys_user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    like_num = db.Column(db.Integer, default=0)
    
    post = db.relationship('CommunityPost', backref=db.backref('comments', lazy=True, cascade="all, delete-orphan"))
    user = db.relationship('User')
