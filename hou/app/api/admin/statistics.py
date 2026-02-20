from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.models.user import User
from app.models.university import University, Major
from app.models.qa import QARecords
from app.utils.response import success_response, error_response
from app.utils.auth import role_required
from sqlalchemy import func

admin_stats_bp = Blueprint('admin_statistics', __name__)

@admin_stats_bp.route('/statistics/dashboard', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_dashboard_stats():
    # 统计数据
    user_count = User.query.count()
    uni_count = University.query.count()
    major_count = Major.query.count()
    qa_count = QARecords.query.count()
    
    # 活跃度模拟
    active_users = [120, 150, 180, 200, 250, 230, 300] # 近7天数据
    
    return success_response({
        "summary": {
            "total_users": user_count,
            "total_universities": uni_count,
            "total_majors": major_count,
            "total_qa": qa_count
        },
        "charts": {
            "active_users": {
                "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                "values": active_users
            }
        }
    })

@admin_stats_bp.route('/statistics/student-source', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_student_source_analysis():
    # 生源省份分布统计
    # 示例返回
    return success_response({
        "provinces": ["广东", "浙江", "江苏", "湖南", "四川"],
        "counts": [500, 300, 250, 200, 150]
    })
