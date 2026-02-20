from app import create_app
from app.models.user import User
from app.extensions import db

app = create_app('development')
with app.app_context():
    user = User.query.filter_by(username='student1').first()
    if user:
        print(f"User found: {user.username}")
        print(f"Role: {user.role}")
        print(f"Hash: {user.password_hash}")
        # Test password
        is_correct = user.check_password('123456')
        print(f"Password '123456' correct: {is_correct}")
    else:
        print("User 'student1' not found in database.")
    
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print(f"Admin found: {admin.username}")
        print(f"Admin hash: {admin.password_hash}")
    else:
        print("Admin user not found.")
