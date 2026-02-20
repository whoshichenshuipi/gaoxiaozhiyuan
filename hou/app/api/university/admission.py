from app.models.university import University, AdmissionScore, Major
from app.models.enrollment_plan import EnrollmentPlan
from flask_jwt_extended import jwt_required, get_jwt
from app.extensions import db
from app.utils.response import success_response, error_response
from app.utils.auth import role_required

uni_adm_bp = Blueprint('university_admission', __name__)

@uni_adm_bp.route('/admission-charter', methods=['POST'])
@jwt_required()
@role_required('university')
def publish_charter():
    data = request.get_json()
    # 逻辑：更新 university 表中的 charter 字段或专门的 charter 表
    return success_response(msg="Charter submitted for review")

@uni_adm_bp.route('/enrollment-plan', methods=['GET'])
@jwt_required()
@role_required('university')
def list_enrollment_plans():
    uni_id = get_jwt().get('university_id')
    plans = EnrollmentPlan.query.filter_by(university_id=uni_id).all()
    return success_response([{
        "id": p.id,
        "year": p.year,
        "province": p.province,
        "major_id": p.major_id,
        "major_name": p.major.name if p.major else "Unknown",
        "plan_num": p.plan_num,
        "requirement": p.requirement,
        "status": p.status
    } for p in plans])

@uni_adm_bp.route('/enrollment-plan', methods=['POST'])
@jwt_required()
@role_required('university')
def add_enrollment_plan():
    uni_id = get_jwt().get('university_id')
    data = request.get_json()
    
    plan = EnrollmentPlan(
        university_id=uni_id,
        year=data.get('year'),
        province=data.get('province'),
        major_id=data.get('major_id'),
        plan_num=data.get('plan_num'),
        requirement=data.get('requirement'),
        status=0 # Pending
    )
    db.session.add(plan)
    db.session.commit()
    return success_response(msg="Enrollment plan added and pending review")

@uni_adm_bp.route('/admission-data', methods=['GET'])
@jwt_required()
@role_required('university')
def list_own_admission_data():
    uni_id = get_jwt().get('university_id')
    scores = AdmissionScore.query.filter_by(university_id=uni_id).all()
    return success_response([{
        "id": s.id,
        "year": s.year,
        "province": s.province,
        "major": s.major.name if s.major else "Unknown",
        "min_score": s.min_score,
        "min_rank": s.min_rank,
        "status": s.status
    } for s in scores])

@uni_adm_bp.route('/admission-data/import', methods=['POST'])
@jwt_required()
@role_required('university')
def import_admission_data():
    # 使用 pandas 解析上传的文件
    # 这里目前返回模拟成功，实际联调时对接文件对象
    return success_response(msg="Data imported successfully")
