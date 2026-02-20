import os
import oss2
from flask import current_app
from werkzeug.utils import secure_filename
import uuid

def upload_to_local(file):
    """
    上传文件到服务器本地
    """
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    
    if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
        os.makedirs(current_app.config['UPLOAD_FOLDER'])
        
    file.save(upload_path)
    # 返回相对路径或拼接后的 URL
    return unique_filename

def upload_to_oss(file):
    """
    上传文件到阿里云 OSS
    """
    auth = oss2.Auth(
        current_app.config['OSS_ACCESS_KEY_ID'], 
        current_app.config['OSS_ACCESS_KEY_SECRET']
    )
    bucket = oss2.Bucket(
        auth, 
        current_app.config['OSS_ENDPOINT'], 
        current_app.config['OSS_BUCKET_NAME']
    )
    
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    # 获取文件流
    file_data = file.read()
    bucket.put_object(unique_filename, file_data)
    
    # 返回 OSS 访问 URL
    return f"{current_app.config['OSS_BASE_URL']}/{unique_filename}"
