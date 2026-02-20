from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.utils.file_helper import upload_to_local, upload_to_oss
from app.utils.response import success_response, error_response
from flask import current_app

common_bp = Blueprint('common', __name__)

@common_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return error_response(msg="No file part")
        
    file = request.files['file']
    if file.filename == '':
        return error_response(msg="No selected file")
        
    # 根据配置选择上传方式，默认优先 OSS (如果已配置)
    try:
        if current_app.config.get('OSS_ACCESS_KEY_ID'):
            url = upload_to_oss(file)
        else:
            url = upload_to_local(file)
            
        return success_response({"url": url})
    except Exception as e:
        return error_response(msg=str(e))
