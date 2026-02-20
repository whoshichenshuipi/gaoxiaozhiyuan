from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.community import CommunityPost, CommunityComment
from app.extensions import db
from app.utils.response import success_response, error_response
from app.utils.auth import role_required

comm_bp = Blueprint('student_community', __name__)

@comm_bp.route('/community/posts', methods=['GET'])
def list_posts():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 20, type=int)
    
    pagination = CommunityPost.query.filter_by(status=1)\
        .order_by(CommunityPost.top_flag.desc(), CommunityPost.create_time.desc())\
        .paginate(page=page, per_page=page_size)
        
    return success_response({
        "list": [{
            "id": p.id,
            "title": p.title,
            "author": p.user.username,
            "like_num": p.like_num,
            "comment_num": len(p.comments),
            "create_time": p.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "top_flag": p.top_flag
        } for p in pagination.items],
        "total": pagination.total
    })

@comm_bp.route('/community/posts', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    post = CommunityPost(
        user_id=user_id,
        title=data.get('title'),
        content=data.get('content')
    )
    db.session.add(post)
    db.session.commit()
    return success_response(msg="Post created")

@comm_bp.route('/community/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    return success_response({
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author": post.user.username,
        "create_time": post.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        "like_num": post.like_num
    })

@comm_bp.route('/community/posts/<int:post_id>/comments', methods=['GET'])
def list_comments(post_id):
    comments = CommunityComment.query.filter_by(post_id=post_id).all()
    return success_response([{
        "id": c.id,
        "content": c.content,
        "author": c.user.username,
        "create_time": c.create_time.strftime("%Y-%m-%d %H:%M:%S")
    } for c in comments])
