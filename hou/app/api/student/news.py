from flask import Blueprint, request
from app.models.news import News
from app.utils.response import success_response

news_bp = Blueprint('student_news', __name__)

@news_bp.route('/news', methods=['GET'])
def list_news():
    news_type = request.args.get('type') # 政策, 技巧, 公告
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 20, type=int)
    
    query = News.query.filter_by(status=1)
    if news_type:
        query = query.filter_by(type=news_type)
        
    pagination = query.order_by(News.top_flag.desc(), News.create_time.desc()).paginate(page=page, per_page=page_size)
    
    return success_response({
        "list": [{
            "id": n.id,
            "title": n.title,
            "type": n.type,
            "create_time": n.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "top_flag": n.top_flag
        } for n in pagination.items],
        "total": pagination.total
    })

@news_bp.route('/news/<int:news_id>', methods=['GET'])
def get_news_detail(news_id):
    news = News.query.get_or_404(news_id)
    return success_response({
        "id": news.id,
        "title": news.title,
        "content": news.content,
        "type": news.type,
        "create_time": news.create_time.strftime("%Y-%m-%d %H:%M:%S")
    })
