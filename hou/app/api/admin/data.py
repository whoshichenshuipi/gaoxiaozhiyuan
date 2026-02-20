from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.models.university import University, Major, AdmissionScore
from app.extensions import db
from app.utils.response import success_response, error_response
from app.utils.auth import role_required
import openpyxl

admin_data_bp = Blueprint('admin_data', __name__)

@admin_data_bp.route('/universities', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_university():
    data = request.get_json()
    uni = University(
        name=data.get('name'),
        level=data.get('level'),
        region=data.get('region'),
        intro=data.get('intro'),
        official_url=data.get('official_url')
    )
    db.session.add(uni)
    db.session.commit()
    return success_response(msg="University added")

@admin_data_bp.route('/admission-data/import', methods=['POST'])
@jwt_required()
@role_required('admin')
def import_admission_data():
    if 'file' not in request.files:
        return error_response(msg="No file part")
    file = request.files['file']
    
    try:
        wb = openpyxl.load_workbook(file)
        sheet = wb.active
        count = 0
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # 格式: 院校ID, 专业ID, 年份, 省份, 最高分, 最低位次, 平均分, 计划数
            uni_id, major_id, year, province, min_s, min_r, avg_s, plan = row
            score = AdmissionScore(
                university_id=uni_id,
                major_id=major_id,
                year=year,
                province=province,
                min_score=min_s,
                min_rank=min_r,
                avg_score=avg_s,
                plan_num=plan,
                status=0 # 待审核
            )
            db.session.add(score)
            count += 1
        db.session.commit()
        return success_response(msg=f"Imported {count} records, pending audit")
    except Exception as e:
        return error_response(msg=f"Import failed: {str(e)}")

@admin_data_bp.route('/admission-data/approve', methods=['POST'])
@jwt_required()
@role_required('admin')
def approve_data():
    data = request.get_json()
    score_ids = data.get('ids', [])
    AdmissionScore.query.filter(AdmissionScore.id.in_(score_ids)).update({"status": 1}, synchronize_session=False)
    db.session.commit()
    return success_response(msg="Data approved")
@admin_data_bp.route('/universities', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_universities():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    name = request.args.get('name')
    
    query = University.query
    if name:
        query = query.filter(University.name.like(f"%{name}%"))
        
    pagination = query.paginate(page=page, per_page=page_size)
    
    return success_response({
        "list": [{
            "id": u.id,
            "name": u.name,
            "level": u.level,
            "region": u.region,
            "official_url": u.official_url
        } for u in pagination.items],
        "total": pagination.total
    })
