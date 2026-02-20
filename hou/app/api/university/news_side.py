from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.models.news import News
from app.extensions import db
from app.utils.response import success_response, error_response
from app.utils.auth import role_required
from datetime import datetime

uni_news_bp = Blueprint('university_news_side', __name__)

@uni_news_bp.route('/news', methods=['GET'])
@jwt_required()
@role_required('university')
def list_uni_news():
    uni_id = get_jwt().get('university_id')
    user_id = get_jwt_identity()
    news_list = News.query.filter_by(publisher_id=user_id).order_by(News.create_time.desc()).all()
    return success_response([{
        "id": n.id,
        "title": n.title,
        "content": n.content,
        "type": n.type,
        "top_flag": n.top_flag,
        "create_time": n.create_time.strftime("%Y-%m-%d %H:%M:%S")
    } for n in news_list])

@uni_news_bp.route('/news', methods=['POST'])
@jwt_required()
@role_required('university')
def publish_uni_news():
    user_id = get_jwt_identity()
    data = request.get_json()
    news = News(
        title=data.get('title'),
        content=data.get('content'),
        type=data.get('type', '公告'),
        publisher_id=user_id,
        publisher_type='university',
        top_flag=data.get('top_flag', False)
    )
    db.session.add(news)
    db.session.commit()
    return success_response(msg="News published")

@uni_news_bp.route('/news/<int:news_id>', methods=['PUT', 'DELETE'])
@jwt_required()
@role_required('university')
def manage_uni_news(news_id):
    user_id = get_jwt_identity()
    news = News.query.filter_by(id=news_id, publisher_id=user_id).first_or_404()
    
    if request.method == 'DELETE':
        db.session.delete(news)
        db.session.commit()
        return success_response(msg="News deleted")
        
    data = request.get_json()
    news.title = data.get('title', news.title)
    news.content = data.get('content', news.content)
    news.type = data.get('type', news.type)
    news.top_flag = data.get('top_flag', news.top_flag)
    db.session.commit()
    return success_response(msg="News updated")
