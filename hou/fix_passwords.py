import pymysql
import bcrypt

# 生成 123456 的正确 Hash
pwd_hash = bcrypt.hashpw(b'123456', bcrypt.gensalt()).decode('utf-8')

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='gaokao_zhiyuan',
        charset='utf8mb4'
    )
    with conn.cursor() as cursor:
        print("正在清理并更新用户数据...")
        # 确保 admin 用户存在
        cursor.execute("DELETE FROM sys_user WHERE username='admin'")
        cursor.execute(f"INSERT INTO sys_user (username, password_hash, role, status) VALUES ('admin', '{pwd_hash}', 'admin', 1)")
        
        # 更新所有考生的密码为 123456
        cursor.execute(f"UPDATE sys_user SET password_hash='{pwd_hash}' WHERE role='student'")
        
        conn.commit()
        print("✅ 修复完成！")
        print(f"管理员账号: admin / 123456")
        print(f"考生账号示例: student1 / 123456")
    conn.close()
except Exception as e:
    print(f"❌ 修复失败: {e}")
