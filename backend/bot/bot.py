from app import *
import requests
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/login_bot', methods=['POST'])
def login_bot():
    username = request.get_json()['username']
    password = request.get_json()['password']
    username_sign = User.query.filter_by(username=username).first()
    print(username_sign)
    if username_sign and check_password_hash(username_sign.password, password):
        if username_sign.student:
            print(username_sign)
            role = 'Student'
            data = {
                'username': username_sign.username, 'role': role
            }
            return jsonify({
                'data': data
            })


@app.route('/student_daily_table_bot', methods=['POST'])
def student_daily_table_bot():
    user_id = request.get_json()['user_id']
    username = request.get_json()['username']

    user = Student.query.filter(Student.id == user_id, Student.classes).first()
    # if user:
    #     data = {
    #         'username': username_sign.username, 'role': role
    #     }
    #     for table in user.classes:
    #         print(username_sign)
    #         role = 'Student'
    #
    #     return jsonify({
    #         'data': data
    #     })
