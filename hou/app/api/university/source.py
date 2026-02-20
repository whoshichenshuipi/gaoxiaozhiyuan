from app.models.volunteer import VolunteerPlan
from app.models.user import StudentProfile, User
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import func
from app.utils.auth import role_required

uni_source_bp = Blueprint('university_source', __name__)

@uni_source_bp.route('/student-source', methods=['GET'])
@jwt_required()
@role_required('university')
def get_student_source():
    # 使用真实的 volunteer_plan 和 student_profile 聚合数据
    uni_id = get_jwt().get('university_id')
    
    # 1. 总量（加入备选库或模拟方案的考生）
    total_interested = VolunteerPlan.query.filter_by(university_id=uni_id).count()
    
    # 2. 分数分布
    # 逻辑：查找关联了该校的所有考生的画像
    student_ids = db.session.query(VolunteerPlan.user_id).filter_by(university_id=uni_id).distinct()
    scores = db.session.query(StudentProfile.score).filter(StudentProfile.user_id.in_(student_ids)).all()
    
    score_dist = {"600+": 0, "550-600": 0, "500-550": 0, "<500": 0}
    for (s,) in scores:
        if s is None: continue
        if s >= 600: score_dist["600+"] += 1
        elif s >= 550: score_dist["550-600"] += 1
        elif s >= 500: score_dist["500-550"] += 1
        else: score_dist["<500"] += 1
            
    # 3. 生源地统计 (基于 StudentProfile.province)
    provinces = db.session.query(
        StudentProfile.province, 
        func.count(StudentProfile.id)
    ).filter(StudentProfile.user_id.in_(student_ids)).group_by(StudentProfile.province).all()
    
    top_provinces = [{"name": p, "value": count} for p, count in provinces]
    top_provinces.sort(key=lambda x: x['value'], reverse=True)
    
    return success_response({
        "total_interested": total_interested,
        "score_distribution": score_dist,
        "top_provinces": top_provinces[:10]  # TOP 10
    })
