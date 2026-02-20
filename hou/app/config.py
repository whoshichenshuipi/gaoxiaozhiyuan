import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'gaokao-secret-key-2024')
    DEBUG = False

    # MySQL
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:123456@localhost:3306/gaokao_zhiyuan?charset=utf8mb4'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'pool_size': 10,
        'max_overflow': 20,
    }

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-2024')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # 文件上传
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'doc'}

    # 阿里云 OSS
    OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID', '')
    OSS_ACCESS_KEY_SECRET = os.getenv('OSS_ACCESS_KEY_SECRET', '')
    OSS_BUCKET_NAME = os.getenv('OSS_BUCKET_NAME', 'gaokao-zhiyuan')
    OSS_ENDPOINT = os.getenv('OSS_ENDPOINT', 'https://oss-cn-hangzhou.aliyuncs.com')
    OSS_BASE_URL = os.getenv('OSS_BASE_URL', '')

    # Qwen3 (DashScope OpenAI 兼容模式)
    DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY', '')
    LLM_MODEL = os.getenv('LLM_MODEL', 'qwen3-235b-a22b')
    LLM_BASE_URL = os.getenv('LLM_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')

    # 日志
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
