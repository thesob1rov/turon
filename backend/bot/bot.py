from app import *
import requests
import json
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import string
import pprint


@app.route('/login_bot', methods=['POST'])
def login_bot():
    username = request.get_json()['username']
    password = request.get_json()['password']
    username_sign = User.query.filter_by(username=username).first()
    if username_sign and check_password_hash(username_sign.password, password):
        if username_sign.student:
            role = 'Student'
            data = {
                'user_id': username_sign.id,
                'username': username_sign.username, 'role': role
            }
            return jsonify({
                'data': data
            })


def get_day_table(day, class_lessons):
    data = []
    this_day = TimeTableDay.query.filter(
        TimeTableDay.name == day).first()
    for lesson in class_lessons:
        day_lesson = TimeTableDay.query.filter(TimeTableDay.id == lesson.day_id).first()
        if this_day:
            if day_lesson.name == this_day.name:
                lesson_time = None
                if lesson.lesson_time == 1 or lesson.lesson_time == 3 or lesson.lesson_time == 4 or lesson.lesson_time == 5 or lesson.lesson_time == 7 or lesson.lesson_time == 8 or lesson.lesson_time == 9:
                    if lesson.lesson_time == 1:
                        lesson_time = 1
                    elif lesson.lesson_time == 3:
                        lesson_time = 2
                    elif lesson.lesson_time == 4:
                        lesson_time = 3
                    elif lesson.lesson_time == 5:
                        lesson_time = 4
                    elif lesson.lesson_time == 7:
                        lesson_time = 5
                    elif lesson.lesson_time == 8:
                        lesson_time = 6
                    elif lesson.lesson_time == 9:
                        lesson_time = 7
                    lesson = {
                        'lesson': lesson.subject.name,
                        'lesson_time': lesson_time,
                        'time': {
                            'start': lesson.time_list.start,
                            'end': lesson.time_list.end
                        },
                        'teacher': lesson.teacher.user.name,
                        'rome': lesson.room.name
                    }
                    data.append(lesson)
    return data


@app.route('/get_student_daily_table_bot', methods=['POST'])
def get_student_daily_table_bot():
    user_id = request.get_json()['user_id']
    today = datetime.now()
    today = today.strftime("%A").lower()
    user = Student.query.filter(Student.user_id == user_id).first()

    if user.classes:
        for classes in user.classes:
            if classes.daily_table:
                data = get_day_table(today, classes.daily_table)
                return jsonify({
                    'data': data
                })


@app.route('/get_student_table_bot', methods=['POST'])
def get_student_table_bot():
    user_id = request.get_json()['user_id']
    user = Student.query.filter(Student.user_id == user_id).first()
    if user.classes:

        for classes in user.classes:
            if classes.daily_table:
                data = []
                day_all = TimeTableDay.query.order_by(TimeTableDay.id).all()
                for day in day_all:
                    day = {
                        'day_name': day.name,
                        'day_lessons': get_day_table(day.name, classes.daily_table)
                    }
                    data.append(day)
                return jsonify({
                    'data': data
                })


@app.route('/get_class_teacher_bot', methods=['POST'])
def get_class_teacher_bot():
    user_id = request.get_json()['user_id']
    user = Student.query.filter(Student.user_id == user_id).first()
    if user.classes:
        for classes in user.classes:
            data = {
                'class_name': classes.name,
                'teacher_len': len(classes.teacher),
                'teachers': []
            }
            for teacher in classes.teacher:
                info = {
                    'teacher_name': teacher.user.name,
                    'teacher_subject': teacher.subject.name
                }
                data['teachers'].append(info)
            return jsonify({
                'data': data
            })


@app.route('/get_class_student_bot', methods=['POST'])
def get_class_student_bot():
    user_id = request.get_json()['user_id']
    user = Student.query.filter(Student.user_id == user_id).first()
    if user.classes:
        for classes in user.classes:
            data = {
                'class_name': classes.name,
                'student_len': len(classes.student),
                'students': []
            }
            for student in classes.student:
                info = {
                    'student_name': student.user.name
                }
                data['students'].append(info)
            print(data)
            return jsonify({
                'data': data
            })


@app.route('/get_student_month_payments_bot', methods=['POST'])
def get_student_month_payments_bot():
    user_id = request.get_json()['user_id']
    user = Student.query.filter(Student.user_id == user_id).first()
    user_payments = StudentMonthPayments.query.filter(StudentMonthPayments.student_id == user.id).all()
    data = []
    for pay in user_payments:
        if pay.payed <= pay.class_price:
            info = {
                'class_price': pay.class_price,
                'payed': pay.payed,
                'month': pay.month.strftime("%Y-%m-%d"),
            }
            data.append(info)
    return jsonify({
        'data': data
    })


@app.route('/get_student_month_in_payments_bot', methods=['POST'])
def get_student_month_in_payments_bot():
    user_id = request.get_json()['user_id']
    user = Student.query.filter(Student.user_id == user_id).first()
    user_payments = StudentMonthPayments.query.filter(StudentMonthPayments.student_id == user.id).all()
    data = []
    today = datetime.now()
    this_month = today.strftime("%m")
    this_year = today.strftime("%Y")
    for pay in user_payments:
        if pay.student_payments_in_month:
            if pay.month.strftime("%Y") == this_year and pay.month.strftime("%m") >= this_month:
                info = {
                    'month': pay.month.strftime("%Y-%m-%d"),
                    'payments': []
                }
                for pay_in in pay.student_payments_in_month:
                    info_pay = {
                        'date': pay_in.date.strftime("%Y-%m-%d"),
                        'payed': pay_in.payed,
                        'account_type': pay_in.account_type.name
                    }
                    info['payments'].append(info_pay)
                data.append(info)
    return jsonify({
        'data': data
    })


@app.route('/get_student_data_bot', methods=['POST'])
def get_student_data_bot():
    user_id = request.get_json()['user_id']
    user = User.query.filter(User.id == user_id).first()
    data = {
        'username': user.username,
        'name': user.name,
        'surname': user.surname,
        'parent_name': user.parent_name,
        'number': user.number,
        'email': user.email,
        'age': user.age
    }
    return jsonify({
        'data': data
    })
