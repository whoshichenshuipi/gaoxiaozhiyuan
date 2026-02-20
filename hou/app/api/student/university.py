from flask import Blueprint, request
from app.models.university import University, Major, AdmissionScore
from app.utils.response import success_response
from sqlalchemy import or_

uni_bp = Blueprint('student_university', __name__)

@uni_bp.route('/universities', methods=['GET'])
def list_universities():
    name = request.args.get('name')
    region = request.args.get('region')
    level = request.args.get('level')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 20, type=int)
    
    query = University.query.filter_by(status=1)
    if name:
        query = query.filter(University.name.like(f"%{name}%"))
    if region:
        query = query.filter(University.region == region)
    if level:
        query = query.filter(University.level == level)
        
    pagination = query.paginate(page=page, per_page=page_size, error_out=False)
    universities = [{
        "id": u.id,
        "name": u.name,
        "level": u.level,
        "region": u.region,
        "official_url": u.official_url
    } for u in pagination.items]
    
    return success_response({
        "list": universities,
        "total": pagination.total,
        "page": page
    })

@uni_bp.route('/universities/<int:uni_id>', methods=['GET'])
def get_university_detail(uni_id):
    uni = University.query.get_or_404(uni_id)
    majors = Major.query.filter_by(university_id=uni_id).all()
    scores = AdmissionScore.query.filter_by(university_id=uni_id).order_by(AdmissionScore.year.desc()).all()
    
    return success_response({
        "info": {
            "id": uni.id,
            "name": uni.name,
            "level": uni.level,
            "region": uni.region,
            "intro": uni.intro,
            "official_url": uni.official_url
        },
        "majors": [{"id": m.id, "name": m.name, "category": m.category} for m in majors],
        "admission_data": [{
            "year": s.year,
            "province": s.province,
            "major_name": s.major.name if s.major else "Unknown",
            "min_score": s.min_score,
            "min_rank": s.min_rank,
            "plan_num": s.plan_num
        } for s in scores]
    })

@uni_bp.route('/majors', methods=['GET'])
def list_majors():
    name = request.args.get('name')
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 20, type=int)
    
    query = Major.query
    if name:
        query = query.filter(Major.name.like(f"%{name}%"))
    if category:
        query = query.filter(Major.category == category)
        
    pagination = query.paginate(page=page, per_page=page_size, error_out=False)
    
    return success_response({
        "list": [{"id": m.id, "name": m.name, "category": m.category, "uni_name": m.university.name} for m in pagination.items],
        "total": pagination.total
    })
