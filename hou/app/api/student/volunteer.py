from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.volunteer import VolunteerPlan
from app.models.university import AdmissionScore
from app.extensions import db
from app.utils.response import success_response, error_response
from app.utils.auth import role_required

vol_bp = Blueprint('volunteer', __name__)

@vol_bp.route('/volunteer', methods=['GET'])
@jwt_required()
@role_required('student')
def list_plans():
    user_id = get_jwt_identity()
    plan_type = request.args.get('type') # 备选库, 模拟方案
    
    query = VolunteerPlan.query.filter_by(user_id=user_id)
    if plan_type:
        query = query.filter_by(type=plan_type)
        
    plans = query.order_by(VolunteerPlan.priority.desc()).all()
    return success_response([{
        "id": p.id,
        "type": p.type,
        "university": p.university.name,
        "major": p.major.name,
        "priority": p.priority,
        "create_time": p.create_time.strftime("%Y-%m-%d %H:%M:%S")
    } for p in plans])

@vol_bp.route('/volunteer', methods=['POST'])
@jwt_required()
@role_required('student')
def add_plan():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    plan = VolunteerPlan(
        user_id=user_id,
        type=data.get('type'),
        university_id=data.get('university_id'),
        major_id=data.get('major_id'),
        priority=data.get('priority', 0)
    )
    db.session.add(plan)
    db.session.commit()
    return success_response(msg="Plan added")

@vol_bp.route('/volunteer/<int:plan_id>', methods=['DELETE'])
@jwt_required()
@role_required('student')
def delete_plan(plan_id):
    user_id = get_jwt_identity()
    plan = VolunteerPlan.query.filter_by(id=plan_id, user_id=user_id).first_or_404()
    db.session.delete(plan)
    db.session.commit()
    return success_response(msg="Plan deleted")

@vol_bp.route('/volunteer/analyze', methods=['POST'])
@jwt_required()
@role_required('student')
def analyze_plans():
    # 模拟分析逻辑：对比近 3 年位次，计算风险等级
    # 返回 ECharts 数据格式
    data = request.get_json()
    user_rank = data.get('rank')
    
    # 这里仅作示例：返回一些模拟的风险分布数据
    return success_response({
        "risk_level": "中",
        "chart_data": {
            "categories": ["冲刺", "稳妥", "保底"],
            "data": [3, 5, 2]
        },
        "details": "您的方案中稳妥院校较多，建议增加 1-2 所保底院校以降低风险。"
    })
