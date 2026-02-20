import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from app.config import config
from app.extensions import db, jwt, cors, migrate

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝图 (Blueprints)
    from app.api.auth import auth_bp
    from app.api.common import common_bp
    from app.api.student.profile import student_bp
    from app.api.student.university import uni_bp
    from app.api.student.recommendation import recommend_bp
    from app.api.student.volunteer import vol_bp
    from app.api.student.community import comm_bp
    from app.api.student.news import news_bp
    from app.api.student.feedback import feedback_bp
    from app.api.student.consultation import msg_bp
    from app.api.admin.users import admin_user_bp
    from app.api.admin.data import admin_data_bp
    from app.api.admin.system import admin_sys_bp
    from app.api.admin.statistics import admin_stats_bp
    from app.api.admin.rag import admin_rag_bp
    from app.api.university.info import uni_info_bp
    from app.api.university.admission import uni_adm_bp
    from app.api.university.source import uni_source_bp
    from app.api.university.consultation import uni_msg_bp
    from app.api.university.faq import uni_faq_bp
    from app.api.university.rag import uni_rag_bp
    from app.api.university.news_side import uni_news_bp
    from app.api.university.feedback_side import uni_feedback_bp
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(common_bp, url_prefix='/api')
    app.register_blueprint(student_bp, url_prefix='/api/student')
    app.register_blueprint(uni_bp, url_prefix='/api/student')
    app.register_blueprint(recommend_bp, url_prefix='/api/student')
    app.register_blueprint(vol_bp, url_prefix='/api/student')
    app.register_blueprint(comm_bp, url_prefix='/api/student')
    app.register_blueprint(news_bp, url_prefix='/api/student')
    app.register_blueprint(feedback_bp, url_prefix='/api/student')
    app.register_blueprint(msg_bp, url_prefix='/api/student')
    app.register_blueprint(admin_user_bp, url_prefix='/api/admin')
    app.register_blueprint(admin_data_bp, url_prefix='/api/admin')
    app.register_blueprint(admin_sys_bp, url_prefix='/api/admin')
    app.register_blueprint(admin_stats_bp, url_prefix='/api/admin')
    app.register_blueprint(admin_rag_bp, url_prefix='/api/admin')
    app.register_blueprint(uni_info_bp, url_prefix='/api/university')
    app.register_blueprint(uni_adm_bp, url_prefix='/api/university')
    app.register_blueprint(uni_source_bp, url_prefix='/api/university')
    app.register_blueprint(uni_msg_bp, url_prefix='/api/university')
    app.register_blueprint(uni_faq_bp, url_prefix='/api/university')
    app.register_blueprint(uni_rag_bp, url_prefix='/api/university')
    app.register_blueprint(uni_news_bp, url_prefix='/api/university')
    app.register_blueprint(uni_feedback_bp, url_prefix='/api/university')

    # 配置日志
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler(
        app.config['LOG_FILE'], 
        maxBytes=10485760, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Gaokao Zhiyuan Startup')

    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy", "service": "gaokao-zhiyuan-backend"})

    # 全局错误处理
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"code": 404, "msg": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"code": 500, "msg": "Internal server error"}), 500

    return app
