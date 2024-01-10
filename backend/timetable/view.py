from app import *
from backend.settings.settings import *
from backend.timetable.timetable_functions import *
from backend.teacher.teacher_salarys import *


@app.route('/creat_timetable/<int:class_id>', methods=["POST", "GET"])
def creat_timetable(class_id):
    """
    timetable yaratiladigan page sinfni ichidan
    :param class_id: kirilgan classni id si
    :return: timetable objectlarini yuvoradi
    """
    # check_session()
    user = User.query.filter(User.id == 1).first()
    # if not user:
    #     return redirect(url_for('home'))
    classs = Class.query.filter(Class.id == class_id).first()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    subjects = Subject.query.all()
    rooms = Room.query.all()
    teachers = Teacher.query.all()
    days = TimeTableDay.query.all()
    times = TimeList.query.order_by(TimeList.id).all()
    classes = Class.query.filter(Class.deleted_classes == None).all()
    new_days = []
    for day in days:
        info = {
            "day_id": day.id,
            "name": day.name,
            # "lesson_time": time.id,
            "lessons": [
            ]
        }
        for time in times:
            les = {
                "status": False,
                "time_id": time.id,
                "time_count": time.lesson_count,
                "start": time.start,
                "end": time.end
            }
            info["lessons"].append(les)
            for item in day.daily_table:
                if item.class_id == classs.id:
                    for lessons in info["lessons"]:
                        if lessons["time_id"] == item.lesson_time:
                            room = Room.query.filter(Room.id == item.room_id).first()
                            teacher = Teacher.query.filter(Teacher.id == item.teacher_id).first()
                            subject = Subject.query.filter(Subject.id == item.subject_id).first()
                            if item.lesson_time == les["time_id"]:
                                if not room and subject and item.teacher_id:
                                    les.update({
                                        "status": True,
                                        "teacher_id": item.teacher_id,
                                        "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                        "subject_id": item.subject_id,
                                        "subject_name": subject.name,
                                        "lesson_id": item.id
                                    })
                                if not item.teacher_id and subject and room:
                                    les.update({
                                        "status": True,
                                        "room_id": item.room_id,
                                        "room_name": room.name,
                                        "teacher_id": None,
                                        "teacher_name": None,
                                        "subject_id": item.subject_id,
                                        "subject_name": subject.name,
                                        "lesson_id": item.id
                                    })
                                if not subject and room and item.teacher_id:
                                    les.update({
                                        "status": True,
                                        "room_id": item.room_id,
                                        "room_name": room.name,
                                        "teacher_id": item.teacher_id,
                                        "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                        "subject_id": None,
                                        "subject_name": None,
                                        "lesson_id": item.id
                                    })
                                if not room and not item.teacher_id:
                                    les.update({
                                        "status": True,
                                        "room_id": None,
                                        "room_name": None,
                                        "teacher_id": None,
                                        "teacher_name": None,
                                        "subject_id": item.subject_id,
                                        "subject_name": subject.name,
                                        "lesson_id": item.id
                                    })
                                if not room and not subject:
                                    les.update({
                                        "status": True,
                                        "room_id": None,
                                        "room_name": None,
                                        "teacher_id": item.teacher_id,
                                        "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                        "subject_id": None,
                                        "subject_name": None,
                                        "lesson_id": item.id
                                    })
                                if not item.teacher_id and not subject:
                                    les.update({
                                        "status": True,
                                        "room_id": item.room_id,
                                        "room_name": room.name,
                                        "teacher_id": None,
                                        "teacher_name": None,
                                        "subject_id": None,
                                        "subject_name": None,
                                        "lesson_id": item.id
                                    })
                                if item.teacher_id and subject and room:
                                    les.update({
                                        "status": True,
                                        "room_id": item.room_id,
                                        "room_name": room.name,
                                        "teacher_id": item.teacher_id,
                                        "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                        "subject_id": item.subject_id,
                                        "subject_name": subject.name,
                                        "lesson_id": item.id
                                    })
        new_days.append(info)
    return render_template('creat_timetable/table.html', about_us=about_us, news=news, jobs=jobs, about_id=about_id,
                           user=user, rooms=rooms, subjects=subjects, teachers=teachers, days=days, times=times,
                           classs=classs, new_days=new_days, classes=classes)


@app.route('/timetables', methods=["POST", "GET"])
def timetables():
    """
    timetable yaratiladigan page
    :return: timetable objectlari yuvoriladi
    """
    calculate_teacher_salary()
    user = User.query.filter(User.id == 1).first()
    # if not user:
    #     return redirect(url_for('home'))
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    subjects = Subject.query.all()
    rooms = Room.query.all()
    teachers = Teacher.query.all()
    days = TimeTableDay.query.all()
    times = TimeList.query.order_by(TimeList.id).all()
    classes = Class.query.filter(Class.deleted_classes == None).all()
    classes2 = Class.query.first()
    time_table = []
    for day in days:
        info = {
            "day": {
                "id": day.id,
                "name": day.name
            },
            "class": {
                "id": classes2.id,
                "name": classes2.name,
                "color": classes2.color,
                "class_number": classes2.class_number,
            },
            "lessons": []
        }

        for time in times:
            daily_table = DailyTable.query.filter(DailyTable.day_id == day.id,
                                                  DailyTable.class_id == classes2.id,
                                                  DailyTable.lesson_time == time.id).order_by(
                DailyTable.lesson_time).first()
            if daily_table:
                flow_info = None
                room_info = None
                teacher_info = None
                subject_info = None
                status = False
                if daily_table.lesson_time == time.id:
                    status = True
                    if daily_table.room:
                        room_info = {
                            "id": daily_table.room.id,
                            "name": daily_table.room.name,
                        }
                    if daily_table.flow:
                        if daily_table.flow_lesson == True:
                            flow_info = {
                                "id": daily_table.flow.id,
                                "name": daily_table.flow.name
                            }
                    if daily_table.teacher:
                        teacher_info = {
                            "id": daily_table.teacher.id,
                            "name": daily_table.teacher.user.name,
                            "surname": daily_table.teacher.user.surname,
                        }
                    if daily_table.subject:
                        subject_info = {
                            "id": daily_table.subject.id,
                            "name": daily_table.subject.name,
                        }
                    info_day = {
                        "lesson_time": {
                            "id": time.id,
                            "start": time.start,
                            "end": time.end,
                            "status": status,
                            "count": time.lesson_count
                        },
                        "room": room_info,
                        "teacher": teacher_info,
                        "subject": subject_info,
                        "flow": flow_info,
                        "lesson_id": daily_table.id
                    }
                    info["lessons"].append(info_day)
            else:
                info_day = {
                    "lesson_time": {
                        "id": time.id,
                        "start": time.start,
                        "end": time.end,
                        "status": False,
                        "count": time.lesson_count
                    },

                }
                info["lessons"].append(info_day)
        time_table.append(info)
    return render_template('timetables/index.html', about_us=about_us, news=news, jobs=jobs, about_id=about_id,
                           user=user, rooms=rooms, time_table=time_table, subjects=subjects, teachers=teachers,
                           days=days, times=times, classes=classes)


@app.route('/get_time_table', methods=["POST", "GET"])
def get_time_table():
    class_id = request.get_json()["class_id"]
    days = TimeTableDay.query.all()
    times = TimeList.query.order_by(TimeList.id).all()
    classes = Class.query.filter(Class.deleted_classes == None).all()
    classes2 = Class.query.filter(Class.id == class_id).first()
    time_table = []

    for day in days:
        info = {
            "day": {
                "id": day.id,
                "name": day.name
            },
            "class": {
                "id": classes2.id,
                "name": classes2.name,
                "color": classes2.color,
                "class_number": classes2.class_number,
            },
            "lessons": [],
            "times": []
        }

        for time in times:
            time_info = {
                "id": time.id,
                "time_count": time.lesson_count,
                "start": time.start,
                "end": time.end,
            }
            info["times"].append(time_info)
            daily_table = DailyTable.query.filter(DailyTable.day_id == day.id,
                                                  DailyTable.class_id == classes2.id,
                                                  DailyTable.lesson_time == time.id).order_by(
                DailyTable.lesson_time).first()
            if daily_table:
                flow_info = None
                room_info = None
                teacher_info = None
                subject_info = None
                status = False
                if daily_table.lesson_time == time.id:
                    status = True
                    if daily_table.room:
                        room_info = {
                            "id": daily_table.room.id,
                            "name": daily_table.room.name,
                        }
                    if daily_table.flow:
                        if daily_table.flow_lesson == True:
                            flow_info = {
                                "id": daily_table.flow.id,
                                "name": daily_table.flow.name
                            }
                    if daily_table.teacher:
                        teacher_info = {
                            "id": daily_table.teacher.id,
                            "name": daily_table.teacher.user.name,
                            "surname": daily_table.teacher.user.surname,
                        }
                    if daily_table.subject:
                        subject_info = {
                            "id": daily_table.subject.id,
                            "name": daily_table.subject.name,
                        }
                    info_day = {
                        "lesson_time": {
                            "id": time.id,
                            "start": time.start,
                            "end": time.end,
                            "status": status,
                            "count": time.lesson_count
                        },
                        "room": room_info,
                        "teacher": teacher_info,
                        "subject": subject_info,
                        "flow": flow_info,
                        "lesson_id": daily_table.id
                    }
                    info["lessons"].append(info_day)
            else:
                info_day = {
                    "lesson_time": {
                        "id": time.id,
                        "start": time.start,
                        "end": time.end,
                        "status": False,
                        "count": time.lesson_count
                    },
                }
                info["lessons"].append(info_day)
        time_table.append(info)
    return jsonify(time_table)


@app.route('/creat_table', methods=["POST"])
def creat_table():
    """
    dars jadali yaratiladigan finksiya
    :return: dars jadvali yaralishi uchun teaherni telshiradi check_teacher_timetable funksiyasiga ma'lumotalni yovoradi
    """
    info = request.get_json()["info"]
    day = TimeTableDay.query.filter(TimeTableDay.id == info["day_id"]).first()
    teacher = Teacher.query.filter(Teacher.id == info["teacher_id"]).first()
    room = Room.query.filter(Room.id == info["room_id"]).first()

    return jsonify({
        "status": check_teacher_timetable(teacher_id=info["teacher_id"], day_id=info["day_id"],
                                          lesson_time_id=info["lesson_time"], room_id=info["room_id"],
                                          subject_id=info["subject_id"], class_id=info["class_id"],
                                          lesson_id=info["lesson_id"])
    })


@app.route('/delete_item_in_lesson', methods=["POST", "GET"])
def delete_item_in_lesson():
    """
    darslikdan teacher xona yoki subjectni optashidigan funksiya
    :return:
    """
    info = request.get_json()["info"]
    time_table_day = TimeTableDay.query.filter(TimeTableDay.id == info["time_table_day_id"]).first()
    if info["text"] == "room":
        DailyTable.query.filter(DailyTable.id == info["lesson_id"]).update({
            "room_id": None
        })
        db.session.commit()
    if info["text"] == "subject":
        DailyTable.query.filter(DailyTable.id == info["lesson_id"]).update({
            "subject_id": None
        })
        db.session.commit()
    if info["text"] == "teacher":
        DailyTable.query.filter(DailyTable.id == info["lesson_id"]).update({
            "teacher_id": None
        })
        db.session.commit()
        calculate_teacher_salary()
    daily_table_all_none = DailyTable.query.filter(DailyTable.id == info["lesson_id"],
                                                   DailyTable.subject_id == None, DailyTable.room_id == None,
                                                   DailyTable.teacher_id == None).first()
    if daily_table_all_none:
        time_table_day.daily_table.remove(daily_table_all_none)
        db.session.commit()
        db.session.delete(daily_table_all_none)
        db.session.commit()
        calculate_teacher_salary()
    return jsonify()


@app.route('/flow_timetable', methods=["POST", "GET"])
def flow_timetable():
    """
    patok yaratildigan page
    :return:
    """
    user = User.query.filter(User.id == 1).first()
    # if not user:
    #     return redirect(url_for('home'))
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    subjects = Subject.query.all()
    rooms = Room.query.all()
    teachers = Teacher.query.all()
    days = TimeTableDay.query.all()
    times = TimeList.query.order_by(TimeList.id).all()
    classes = Class.query.all()
    # day_list = flow_student__table_information()
    flow_types = [
        {
            "classes": "1, 2, 3, 4",
            "color": "blue",
            "start": 1,
            "end": 4,
        },
        {
            "classes": "5, 6",
            "color": "blue",
            "start": 5,
            "end": 6,
        },
        {
            "classes": "7, 8, 9",
            "color": "blue",
            "start": 7,
            "end": 9,
        },
        {
            "classes": "1, 2, 3, 4",
            "color": "green",
            "start": 1,
            "end": 4,
        },
        {
            "classes": "5, 6",
            "color": "green",
            "start": 5,
            "end": 6,
        },
        {
            "classes": "7, 8, 9",
            "color": "green",
            "start": 7,
            "end": 9,
        },
    ]
    class_list = [1, 2, 3, 4]
    class_list2 = "1, 2, 3, 4"
    color = "blue"
    flows = Flow.query.all()
    days = TimeTableDay.query.all()
    times = TimeList.query.order_by(TimeList.id).all()
    time_table = []
    for day in days:
        info = {
            "day": {
                "id": day.id,
                "name": day.name
            },
            "lessons": [],
            "times": []
        }
        for time in times:
            time_info = {
                "id": time.id,
                "time_count": time.lesson_count,
                "start": time.start,
                "end": time.end,
            }
            info["times"].append(time_info)
            # daily_table = DailyTable.query.filter(DailyTable.day_id == day.id,
            #                                       DailyTable.lesson_time == time.id,
            #                                       DailyTable.flow_lesson == True).order_by(
            #     DailyTable.lesson_time).first()
            daily_table = db.session.query(DailyTable).join(DailyTable.class_get).options(
                contains_eager(DailyTable.class_get)).filter(Class.class_number.in_(class_list),
                                                             Class.color == color,
                                                             DailyTable.day_id == day.id,
                                                             DailyTable.lesson_time == time.id,
                                                             DailyTable.flow_lesson == True).order_by(
                DailyTable.lesson_time).first()
            if daily_table:
                flow_info = None
                room_info = None
                status = False
                if daily_table.lesson_time == time.id:
                    status = True
                    if daily_table.room:
                        room_info = {
                            "id": daily_table.room.id,
                            "name": daily_table.room.name,
                        }
                    if daily_table.flow:
                        if daily_table.flow_lesson == True:
                            flow_info = {
                                "id": daily_table.flow.id,
                                "name": daily_table.flow.name
                            }
                    info_day = {
                        "lesson_time": {
                            "id": time.id,
                            "start": time.start,
                            "end": time.end,
                            "status": status,
                            "count": time.lesson_count
                        },
                        "room": room_info,
                        "flow": flow_info,
                        "lesson_id": daily_table.id
                    }
                    info["lessons"].append(info_day)
            else:
                info_day = {
                    "lesson_time": {
                        "id": time.id,
                        "start": time.start,
                        "end": time.end,
                        "status": False,
                        "count": time.lesson_count
                    },
                }
                info["lessons"].append(info_day)
        time_table.append(info)
    return render_template('flow_student/flow_student.html', about_us=about_us, news=news, jobs=jobs, about_id=about_id,
                           user=user, rooms=rooms, subjects=subjects, teachers=teachers, days=days, times=times,
                           flows=flows, time_table=time_table, flow_types=flow_types, classes=classes,
                           class_list2=class_list2, color=color)


@app.route('/get_flow_timetable', methods=["POST", "GET"])
def get_flow_timetable():
    """
    patok yaratildigan page
    :return:
    """
    info_get = request.get_json()["info"]
    print(info_get)
    class_list = None
    if info_get["end"] == "4":
        class_list = [1, 2, 3, 4]
    if info_get["end"] == "6":
        class_list = [5, 6]
    if info_get["end"] == "9":
        class_list = [7, 8, 9]
    days = TimeTableDay.query.all()
    times = TimeList.query.order_by(TimeList.id).all()
    time_table = []
    for day in days:
        info = {
            "day": {
                "id": day.id,
                "name": day.name
            },
            "lessons": [],
            "times": [],
            "classes": class_list,
            "color": info_get["color"]
        }
        for time in times:
            time_info = {
                "id": time.id,
                "time_count": time.lesson_count,
                "start": time.start,
                "end": time.end,
            }
            info["times"].append(time_info)
            # daily_table = DailyTable.query.filter(DailyTable.day_id == day.id,
            #                                       DailyTable.lesson_time == time.id,
            #                                       DailyTable.flow_lesson == True).order_by(
            #     DailyTable.lesson_time).first()
            daily_table = db.session.query(DailyTable).join(DailyTable.class_get).options(
                contains_eager(DailyTable.class_get)).filter(Class.class_number.in_(class_list),
                                                             Class.color == info_get["color"],
                                                             DailyTable.day_id == day.id,
                                                             DailyTable.lesson_time == time.id,
                                                             DailyTable.flow_lesson == True).order_by(
                DailyTable.lesson_time).first()
            if daily_table:
                flow_info = None
                room_info = None
                status = False
                if daily_table.lesson_time == time.id:
                    status = True
                    if daily_table.room:
                        room_info = {
                            "id": daily_table.room.id,
                            "name": daily_table.room.name,
                        }
                    if daily_table.flow:
                        if daily_table.flow_lesson == True:
                            flow_info = {
                                "id": daily_table.flow.id,
                                "name": daily_table.flow.name
                            }
                    info_day = {
                        "lesson_time": {
                            "id": time.id,
                            "start": time.start,
                            "end": time.end,
                            "status": status,
                            "count": time.lesson_count
                        },
                        "room": room_info,
                        "flow": flow_info,
                        "lesson_id": daily_table.id
                    }
                    info["lessons"].append(info_day)
            else:
                info_day = {
                    "lesson_time": {
                        "id": time.id,
                        "start": time.start,
                        "end": time.end,
                        "status": False,
                        "count": time.lesson_count
                    },
                }
                info["lessons"].append(info_day)
        time_table.append(info)
    return jsonify(time_table)


#     flows = Flow.query.all()
#     days = TimeTableDay.query.all()
#     times = TimeList.query.order_by(TimeList.id).all()
#     time_table = []
#     for day in days:
#         info = {
#             "day": {
#                 "id": day.id,
#                 "name": day.name
#             },
#             "lessons": [],
#             "times": []
#         }
#         for time in times:
#             time_info = {
#                 "id": time.id,
#                 "time_count": time.lesson_count,
#                 "start": time.start,
#                 "end": time.end,
#             }
#             info["times"].append(time_info)
#             daily_table = DailyTable.query.filter(DailyTable.day_id == day.id,
#                                                   DailyTable.lesson_time == time.id,
#                                                   DailyTable.flow_lesson == True).order_by(
#                 DailyTable.lesson_time).first()
#             if daily_table:
#                 flow_info = None
#                 room_info = None
#                 status = False
#                 if daily_table.lesson_time == time.id:
#                     status = True
#                     if daily_table.room:
#                         room_info = {
#                             "id": daily_table.room.id,
#                             "name": daily_table.room.name,
#                         }
#                     if daily_table.flow_lesson == True:
#                         flow_info = {
#                             "id": daily_table.flow.id,
#                             "name": daily_table.flow.name
#                         }
#                     info_day = {
#                         "lesson_time": {
#                             "id": time.id,
#                             "start": time.start,
#                             "end": time.end,
#                             "status": status,
#                             "count": time.lesson_count
#                         },
#                         "room": room_info,
#                         "flow": flow_info,
#                         "lesson_id": daily_table.id
#                     }
#                     info["lessons"].append(info_day)
#             else:
#                 info_day = {
#                     "lesson_time": {
#                         "id": time.id,
#                         "start": time.start,
#                         "end": time.end,
#                         "status": False,
#                         "count": time.lesson_count
#                     },
#                 }
#                 info["lessons"].append(info_day)
#         time_table.append(info)

@app.route('/creat_flow_timetable', methods=["POST", "GET"])
def creat_flow_timetable():
    """
    patok yaratadi
    :return: patok uchun teacherni voxtini tekshiradigan funksiyaga yuvoradi
    """
    info = request.get_json()["info"]
    return jsonify({
        "status": check_teacher_for_flow_timetable(day_id=info["day_id"],
                                                   lesson_time_id=info["lesson_time"], room_id=info["room_id"],
                                                   lesson_id=info["lesson_id"], flow_id=info["flow_id"])
    })


@app.route('/delete_flow_item_in_lesson', methods=["POST", "GET"])
def delete_flow_item_in_lesson():
    """
    patokdan darsligidan patok yoki xonani optashidigan funksiya
    :return:
    """
    info = request.get_json()["info"]
    time_table_day = TimeTableDay.query.filter(TimeTableDay.id == info["time_table_day_id"]).first()
    if info["text"] == "room":
        DailyTable.query.filter(DailyTable.id == info["lesson_id"]).update({
            "room_id": None
        })
        db.session.commit()
    if info["text"] == "flow":
        DailyTable.query.filter(DailyTable.id == info["lesson_id"]).update({
            "flow_id": None
        })
        db.session.commit()
        calculate_teacher_salary()
    daily_table_all_none = DailyTable.query.filter(DailyTable.id == info["lesson_id"],
                                                   DailyTable.room_id == None,
                                                   DailyTable.flow_id == None).first()
    if daily_table_all_none:
        time_table_day.daily_table.remove(daily_table_all_none)
        db.session.commit()
        db.session.delete(daily_table_all_none)
        db.session.commit()
        calculate_teacher_salary()
    return jsonify()


@app.route('/lesson_table', methods=["POST", "GET"])
def lesson_table():
    """
    tayyor dars jadvalini korish uchun page
    :return:
    """
    user = User.query.filter(User.id == 1).first()
    # if not user:
    #     return redirect(url_for('home'))
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    times = TimeList.query.all()
    lesson_list = lesson_table_list()
    days = TimeTableDay.query.all()

    day = TimeTableDay.query.order_by(TimeTableDay.id).first()
    rooms = Room.query.all()
    time_table = []
    for room in rooms:
        info = {
            "day": {
                "id": day.id,
                "name": day.name
            },
            "room": {
                "id": room.id,
                "name": room.name
            },
            "lessons": [],
            "times": []
        }
        for time in times:
            time_info = {
                "id": time.id,
                "time_count": time.lesson_count,
                "start": time.start,
                "end": time.end,
            }
            info["times"].append(time_info)
            daily_table = DailyTable.query.filter(DailyTable.day_id == day.id,
                                                  DailyTable.lesson_time == time.id).order_by(
                DailyTable.lesson_time).first()
            if daily_table:
                flow_info = None
                room_info = None
                teacher_info = None
                subject_info = None
                status = False
                if daily_table.lesson_time == time.id:
                    status = True
                    if daily_table.room:
                        room_info = {
                            "id": daily_table.room.id,
                            "name": daily_table.room.name,
                        }
                    if daily_table.flow_lesson == True:
                        flow_info = {
                            "id": daily_table.flow.id,
                            "name": daily_table.flow.name
                        }
                    if daily_table.teacher:
                        teacher_info = {
                            "id": daily_table.teacher.id,
                            "name": daily_table.teacher.user.name,
                            "surname": daily_table.teacher.user.surname,
                        }
                    if daily_table.subject:
                        subject_info = {
                            "id": daily_table.subject.id,
                            "name": daily_table.subject.name,
                        }
                    info_day = {
                        "lesson_time": {
                            "id": time.id,
                            "start": time.start,
                            "end": time.end,
                            "status": status,
                            "count": time.lesson_count
                        },
                        "room": room_info,
                        "teacher": teacher_info,
                        "subject": subject_info,
                        "flow": flow_info,
                        "lesson_id": daily_table.id
                    }
                    info["lessons"].append(info_day)
            else:
                info_day = {
                    "lesson_time": {
                        "id": time.id,
                        "start": time.start,
                        "end": time.end,
                        "status": False,
                        "count": time.lesson_count
                    },
                }
                info["lessons"].append(info_day)
        time_table.append(info)
    return render_template('lesson_table/table.html', about_us=about_us, news=news, jobs=jobs, about_id=about_id,
                           user=user, times=times, lesson_list=lesson_list, days=days)
