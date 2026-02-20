import pymysql

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='gaokao_zhiyuan',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    with conn.cursor() as cursor:
        cursor.execute("SELECT username, role, password_hash FROM sys_user WHERE username='student1'")
        user = cursor.fetchone()
        if user:
            print(f"User Found: {user['username']}")
            print(f"Role: {user['role']}")
            print(f"Hash: {user['password_hash']}")
            # Manual check with bcrypt if available
            try:
                import bcrypt
                is_correct = bcrypt.checkpw('123456'.encode('utf-8'), user['password_hash'].encode('utf-8'))
                print(f"Bcrypt check for '123456': {is_correct}")
            except ImportError:
                print("Bcrypt not found in current environment.")
        else:
            cursor.execute("SELECT COUNT(*) as count FROM sys_user")
            count = cursor.fetchone()
            print(f"User 'student1' NOT found. Total users in DB: {count['count']}")
            cursor.execute("SELECT username FROM sys_user LIMIT 5")
            users = cursor.fetchall()
            print(f"Some users in DB: {[u['username'] for u in users]}")
    conn.close()
except Exception as e:
    print(f"Database error: {e}")
