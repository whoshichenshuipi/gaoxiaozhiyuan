from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.models.university import University, AdmissionScore, Major
from app.utils.response import success_response, error_response
from sqlalchemy import and_

recommend_bp = Blueprint('recommendation', __name__)

@recommend_bp.route('/recommendation/generate', methods=['POST'])
@jwt_required()
def generate_recommendation():
    data = request.get_json()
    score = data.get('score')
    rank = data.get('rank')
    province = data.get('province')
    subject = data.get('subject') # e.g., 理科, 文科, 物理类, 历史类
    
    if not all([score, rank, province]):
        return error_response(msg="Missing required parameters")
        
    # 推荐逻辑：位次 ±10% 筛选
    # 冲刺 (Sprint): rank * 0.8 到 rank 之间
    # 稳妥 (Stable): rank 到 rank * 1.2 之间
    # 保底 (Safe): rank * 1.2 以上
    
    def get_list(min_r, max_r):
        scores = AdmissionScore.query.filter(
            AdmissionScore.province == province,
            AdmissionScore.min_rank >= min_r,
            AdmissionScore.min_rank <= max_r,
            AdmissionScore.year == 2023 # 假设以最新一年为基准
        ).limit(10).all()
        
        return [{
            "university_name": s.university.name,
            "major_name": s.major.name,
            "last_min_rank": s.min_rank,
            "last_min_score": s.min_score,
            "plan_num": s.plan_num,
            "level": s.university.level
        } for s in scores]

    sprint = get_list(rank * 0.7, rank)
    stable = get_list(rank, rank * 1.2)
    safe = get_list(rank * 1.2, rank * 2.0)
    
    return success_response({
        "sprint": sprint,
        "stable": stable,
        "safe": safe,
        "summary": f"根据您的位次 {rank}，为您推荐了 {len(sprint)} 所冲刺院校，{len(stable)} 所稳妥院校，以及 {len(safe)} 所保底院校。"
    })
