from datetime import datetime
from app.extensions import db

class QAPromptTemplate(db.Model):
    __tablename__ = 'qa_prompt_template'
    
    id = db.Column(db.Integer, primary_key=True)
    template_type = db.Column(db.String(50), nullable=False)  # 通用, 高校
    template_content = db.Column(db.Text, nullable=False)
    variables = db.Column(db.String(255))
    is_default = db.Column(db.Boolean, default=False)

class KnowledgeBase(db.Model):
    __tablename__ = 'knowledge_base'
    
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    doc_name = db.Column(db.String(255), nullable=False)
    doc_type = db.Column(db.String(50))
    doc_url = db.Column(db.String(255))
    content_chunks = db.Column(db.JSON)  # Store text chunks if not using external vector DB initially
    vector_id = db.Column(db.String(128))
    status = db.Column(db.Integer, default=0) # 0: pending, 1: processed
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    university = db.relationship('University')

class QARecords(db.Model):
    __tablename__ = 'qa_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('sys_user.id'))
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text)
    rag_used = db.Column(db.Boolean, default=False)
    response_time = db.Column(db.Integer)  # in milliseconds
    create_time = db.Column(db.DateTime, default=datetime.now)

class UniversityFAQ(db.Model):
    __tablename__ = 'university_faq'
    
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    sort_weight = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now)
    
    university = db.relationship('University')
