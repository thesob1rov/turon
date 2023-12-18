from app import *
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import string


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
                'user_id': username_sign.id,
                'username': username_sign.username, 'role': role
            }
            return jsonify({
                'data': data
            })


@app.route('/student_daily_table_bot', methods=['POST'])
def student_daily_table_bot():
    user_id = request.get_json()['user_id']
    today = datetime.now()

    user = Student.query.filter(Student.user_id == user_id).first()
    this_day = TimeTableDay.query.filter(
        TimeTableDay.name == today.strftime("%A")[0].lower() + today.strftime("%A")[1]).first()
    # this_day = TimeTableDay.query.filter(TimeTableDay.name == 'tuesday').first()
    if user.classes:
        for classes in user.classes:
            if classes.daily_table:
                data = []
                for lesson in classes.daily_table:
                    day_lesson = TimeTableDay.query.filter(TimeTableDay.id == lesson.day_id).first()
                    print(False)
                    if this_day:
                        if day_lesson.name == this_day.name:
                            if lesson.lesson_time == 1:
                                lesson = {
                                    'lesson': lesson.subject.name,
                                    'time': {
                                        'start': lesson.time_list.start,
                                        'end': lesson.time_list.end
                                    },
                                    'teacher': lesson.teacher.user.name,
                                    'rome': lesson.room.name
                                }
                                data.append(lesson)
                            elif lesson.lesson_time == 3:
                                lesson = {
                                    'lesson': lesson.subject.name,
                                    'time': {
                                        'start': lesson.time_list.start,
                                        'end': lesson.time_list.end
                                    },
                                    'teacher': lesson.teacher.user.name,
                                    'rome': lesson.room.name
                                }
                                data.append(lesson)
                            elif lesson.lesson_time == 4:
                                lesson = {
                                    'lesson': lesson.subject.name,
                                    'time': {
                                        'start': lesson.time_list.start,
                                        'end': lesson.time_list.end
                                    },
                                    'teacher': lesson.teacher.user.name,
                                    'rome': lesson.room.name
                                }
                                data.append(lesson)
                            elif lesson.lesson_time == 5:
                                print(True)
                                lesson = {
                                    'lesson': lesson.subject.name,
                                    'time': {
                                        'start': lesson.time_list.start,
                                        'end': lesson.time_list.end
                                    },
                                    'teacher': lesson.teacher.user.name,
                                    'rome': lesson.room.name
                                }
                                data.append(lesson)
                            elif lesson.lesson_time == 6:
                                lesson = {
                                    'lesson': lesson.subject.name,
                                    'time': {
                                        'start': lesson.time_list.start,
                                        'end': lesson.time_list.end
                                    },
                                    'teacher': lesson.teacher.user.name,
                                    'rome': lesson.room.name
                                }
                                data.append(lesson)
                            elif lesson.lesson_time == 8:
                                lesson = {
                                    'lesson': lesson.subject.name,
                                    'time': {
                                        'start': lesson.time_list.start,
                                        'end': lesson.time_list.end
                                    },
                                    'teacher': lesson.teacher.user.name,
                                    'rome': lesson.room.name
                                }
                                data.append(lesson)
                            elif lesson.lesson_time == 9:
                                lesson = {
                                    'lesson': lesson.subject.name,
                                    'time': {
                                        'start': lesson.time_list.start,
                                        'end': lesson.time_list.end
                                    },
                                    'teacher': lesson.teacher.user.name,
                                    'rome': lesson.room.name
                                }
                                data.append(lesson)
                            else:
                                print(False)
                                lesson = {
                                    'lesson': None,
                                    'time': {
                                        'start': None,
                                        'end': None
                                    },
                                    'teacher': None,
                                    'rome': None
                                }
                                data.append(lesson)
                return jsonify({
                    'data': data
                })


@app.route('/student_table_bot', methods=['POST'])
def student_table_bot():
    user_id = request.get_json()['user_id']
    user = Student.query.filter(Student.user_id == user_id).first()
    if user.classes:
        for classes in user.classes:
            if classes.daily_table:
                data = []
                for lesson in classes.daily_table:
                    if lesson.day_id == 1:
                        day = {
                            'day_name': lesson.day.name
                        }
                        data.append(day)
                    elif lesson.day_id == 2:
                        day = {
                            'day': 1
                        }
                        data.append(day)
                    elif lesson.day_id == 3:
                        day = {
                            'day': 1
                        }
                        data.append(day)
                    elif lesson.day_id == 4:
                        day = {
                            'day': 1
                        }
                        data.append(day)
                    elif lesson.day_id == 5:
                        day = {
                            'day': 1
                        }
                        data.append(day)
                return jsonify({
                    'data': data
                })
