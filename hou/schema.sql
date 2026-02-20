-- 高考志愿服务系统数据库脚本 (MySQL 8.0)

CREATE DATABASE IF NOT EXISTS gaokao_zhiyuan DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gaokao_zhiyuan;

-- 1. 基础权限模块
CREATE TABLE sys_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL COMMENT 'student/admin/university',
    status INT DEFAULT 1 COMMENT '1:可用, 0:禁用, 2:待审核',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login_time DATETIME
) ENGINE=InnoDB;

CREATE TABLE sys_permission (
    id INT AUTO_INCREMENT PRIMARY KEY,
    permission_code VARCHAR(64) UNIQUE NOT NULL,
    permission_name VARCHAR(64) NOT NULL,
    role VARCHAR(20) NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. 考生信息模块
CREATE TABLE student_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    score INT,
    province VARCHAR(32),
    subject_selection VARCHAR(255),
    hobbies TEXT,
    region_preference VARCHAR(255),
    specialty VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 3. 基础院校与录取数据
CREATE TABLE university (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    level VARCHAR(64) COMMENT '985/211/双高/普通',
    region VARCHAR(64),
    intro TEXT,
    official_url VARCHAR(255),
    status INT DEFAULT 1,
    INDEX idx_uni_name (name)
) ENGINE=InnoDB;

CREATE TABLE major (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    category VARCHAR(64),
    discipline VARCHAR(64),
    intro TEXT,
    university_id INT NOT NULL,
    FOREIGN KEY (university_id) REFERENCES university(id) ON DELETE CASCADE,
    INDEX idx_major_name (name)
) ENGINE=InnoDB;

CREATE TABLE admission_score (
    id INT AUTO_INCREMENT PRIMARY KEY,
    university_id INT NOT NULL,
    major_id INT NOT NULL,
    year INT NOT NULL,
    province VARCHAR(64) NOT NULL,
    min_score INT,
    min_rank INT,
    avg_score INT,
    plan_num INT,
    status INT DEFAULT 1,
    FOREIGN KEY (university_id) REFERENCES university(id),
    FOREIGN KEY (major_id) REFERENCES major(id)
) ENGINE=InnoDB;

-- 4. 志愿管理
CREATE TABLE volunteer_plan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type VARCHAR(20) NOT NULL COMMENT '备选库/模拟方案',
    university_id INT NOT NULL,
    major_id INT NOT NULL,
    priority INT DEFAULT 0,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE,
    FOREIGN KEY (university_id) REFERENCES university(id),
    FOREIGN KEY (major_id) REFERENCES major(id)
) ENGINE=InnoDB;

-- 5. 社区功能
CREATE TABLE community_post (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    like_num INT DEFAULT 0,
    status INT DEFAULT 1,
    top_flag BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES sys_user(id)
) ENGINE=InnoDB;

CREATE TABLE community_comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    like_num INT DEFAULT 0,
    FOREIGN KEY (post_id) REFERENCES community_post(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES sys_user(id)
) ENGINE=InnoDB;

-- 6. 资讯管理
CREATE TABLE news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    type VARCHAR(50) COMMENT '政策/技巧/公告',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    top_flag BOOLEAN DEFAULT FALSE,
    publisher_id INT,
    status INT DEFAULT 1,
    FOREIGN KEY (publisher_id) REFERENCES sys_user(id)
) ENGINE=InnoDB;

-- 7. 反馈管理
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type VARCHAR(50) COMMENT '数据异常/功能建议/其他',
    content TEXT NOT NULL,
    screenshot_url VARCHAR(255),
    status INT DEFAULT 0 COMMENT '0:待处理, 1:已回复',
    reply TEXT,
    reply_time DATETIME,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES sys_user(id)
) ENGINE=InnoDB;

-- 8. 咨询互动
CREATE TABLE consultation_message (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    content TEXT NOT NULL,
    msg_type VARCHAR(20) DEFAULT 'text',
    send_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    read_flag BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (sender_id) REFERENCES sys_user(id),
    FOREIGN KEY (receiver_id) REFERENCES sys_user(id)
) ENGINE=InnoDB;

CREATE TABLE leave_message (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    university_id INT NOT NULL,
    content TEXT NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    reply TEXT,
    reply_time DATETIME,
    status INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES sys_user(id),
    FOREIGN KEY (university_id) REFERENCES university(id)
) ENGINE=InnoDB;

-- 9. 智能问答与 RAG
CREATE TABLE qa_prompt_template (
    id INT AUTO_INCREMENT PRIMARY KEY,
    template_type VARCHAR(50) NOT NULL COMMENT '通用/高校',
    template_content TEXT NOT NULL,
    variables VARCHAR(255),
    is_default BOOLEAN DEFAULT FALSE
) ENGINE=InnoDB;

CREATE TABLE knowledge_base (
    id INT AUTO_INCREMENT PRIMARY KEY,
    university_id INT,
    doc_name VARCHAR(255) NOT NULL,
    doc_type VARCHAR(50),
    doc_url VARCHAR(255),
    content_chunks JSON,
    vector_id VARCHAR(128),
    status INT DEFAULT 0,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (university_id) REFERENCES university(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE qa_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    university_id INT,
    question TEXT NOT NULL,
    answer TEXT,
    rag_used BOOLEAN DEFAULT FALSE,
    response_time INT COMMENT '毫秒',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES sys_user(id),
    FOREIGN KEY (university_id) REFERENCES university(id)
) ENGINE=InnoDB;

CREATE TABLE university_faq (
    id INT AUTO_INCREMENT PRIMARY KEY,
    university_id INT NOT NULL,
    question VARCHAR(255) NOT NULL,
    answer TEXT NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (university_id) REFERENCES university(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 10. 系统监控与分析
CREATE TABLE sys_operation_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    operation_type VARCHAR(50),
    content TEXT,
    ip VARCHAR(45),
    operation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES sys_user(id)
) ENGINE=InnoDB;

CREATE TABLE student_source (
    id INT AUTO_INCREMENT PRIMARY KEY,
    university_id INT NOT NULL,
    user_id INT NOT NULL,
    volunteer_type VARCHAR(20),
    score INT,
    province VARCHAR(64),
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (university_id) REFERENCES university(id),
    FOREIGN KEY (user_id) REFERENCES sys_user(id)
) ENGINE=InnoDB;
