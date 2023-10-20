from app import *
from backend.settings.settings import *


def check_teacher_timetable(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id, lesson_id):
    """
    dars jadvalini yaratish uchun teacherni tekshiradigan funksiya
    :param teacher_id: teacherni id si
    :param day_id: kuni id si
    :param lesson_time_id: dars voxtini id is
    :param room_id: xonani id si
    :param subject_id: fanlani id si
    :param class_id: dinf id si
    :param lesson_id: dars id si toldirilmagan darslik bosa oshani id si keladi
    :return: agar teacher etilgan payt bosh bosa kegin check_room_timetable funksiyasigi yuvoradi u funksiya room ni tekshiradi
    """
    teacher = Teacher.query.filter(Teacher.id == teacher_id).first()
    if teacher.daily_table:
        for daily_table in teacher.daily_table:
            if daily_table.day_id == int(day_id) and daily_table.lesson_time == int(lesson_time_id):
                if lesson_id == "":
                    message = {
                        "text": 'bu voxta darsi teacherni',
                        "color": "red"
                    }
                    return message
                else:
                    filter_lesson = DailyTable.query.filter(DailyTable.id == lesson_id).first()
                    if filter_lesson.teacher_id == int(teacher_id):
                        return check_room_timetable(teacher_id=teacher_id, day_id=day_id,
                                                    lesson_time_id=lesson_time_id, room_id=room_id,
                                                    subject_id=subject_id, class_id=class_id, lesson_id=lesson_id)
                    else:
                        message = {
                            "text": 'bu voxta darsi teacherni',
                            "color": "red"
                        }
                        return message
            else:
                return check_room_timetable(teacher_id=teacher_id, day_id=day_id,
                                            lesson_time_id=lesson_time_id, room_id=room_id,
                                            subject_id=subject_id, class_id=class_id, lesson_id=lesson_id)
    else:
        return check_room_timetable(teacher_id=teacher_id, day_id=day_id,
                                    lesson_time_id=lesson_time_id, room_id=room_id,
                                    subject_id=subject_id, class_id=class_id, lesson_id=lesson_id)


def check_room_timetable(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id, lesson_id):
    """
    agar dars jadvaliga yuvorilgan teacherni voxti bosa kegn shu funksiya ishlidi roomlani tekshirib chiqadi voxtini
    :param teacher_id: teacherni id si
    :param day_id: kuni id si
    :param lesson_time_id: dars voxtini id is
    :param room_id: xonani id si
    :param subject_id: fanlani id si
    :param class_id: dinf id si
    :param lesson_id: dars id si toldirilmagan darslik bosa oshani id si keladi
    :return: agar roomni voxti bosa darslikni saqlab olish uchun add_new_daily_table funksiyasiga yuvoradi yoki toldirilmagan darslik bosa uni
     update_old_time_table funksiyasiga yuvoradi va darslkni yangilidi
    """
    room = Room.query.filter(Room.id == room_id).first()
    status = True
    if room.daily_table:
        for daily_table in room.daily_table:
            if daily_table.day_id == int(day_id) and daily_table.lesson_time == int(lesson_time_id):

                if lesson_id == "":
                    message = {
                        "text": 'bu voxtda xona zanet',
                        "color": "red"
                    }
                    status = False
                    return message
                else:
                    filter_lesson = DailyTable.query.filter(DailyTable.id == lesson_id).first()
                    if filter_lesson.room_id == int(room_id):
                        status = False
                        return update_old_time_table(teacher_id=teacher_id, day_id=day_id,
                                                     lesson_time_id=lesson_time_id, room_id=room_id,
                                                     subject_id=subject_id, class_id=class_id, lesson_id=lesson_id)
                    else:
                        message = {
                            "text": 'bu voxtda xona zanet',
                            "color": "red"
                        }
                        status = False
                        return message
        if status == True:

            if lesson_id == "":

                return add_new_daily_table(teacher_id=teacher_id, day_id=day_id,
                                           lesson_time_id=lesson_time_id, room_id=room_id,
                                           subject_id=subject_id, class_id=class_id, lesson_id=lesson_id)
            else:

                return update_old_time_table(teacher_id=teacher_id, day_id=day_id,
                                             lesson_time_id=lesson_time_id, room_id=room_id,
                                             subject_id=subject_id, class_id=class_id, lesson_id=lesson_id)

    else:
        if lesson_id == "":
            return add_new_daily_table(teacher_id=teacher_id, day_id=day_id,
                                       lesson_time_id=lesson_time_id, room_id=room_id,
                                       subject_id=subject_id, class_id=class_id, lesson_id=lesson_id)
        else:
            return update_old_time_table(teacher_id=teacher_id, day_id=day_id,
                                         lesson_time_id=lesson_time_id, room_id=room_id,
                                         subject_id=subject_id, class_id=class_id, lesson_id=lesson_id)


def add_new_daily_table(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id, lesson_id):
    """
    darslikni qoshadi
    :param teacher_id: teacherni id si
    :param day_id: kuni id si
    :param lesson_time_id: dars voxtini id is
    :param room_id: xonani id si
    :param subject_id: fanlani id si
    :param class_id: dinf id si
    :param lesson_id: dars id si toldirilmagan darslik bosa oshani id si keladi
    :return: darslik qoshgani xaqida xabar yuvoradi
    """
    day = TimeTableDay.query.filter(TimeTableDay.id == day_id).first()
    add = DailyTable(teacher_id=teacher_id, subject_id=subject_id, room_id=room_id, class_id=class_id,
                     lesson_time=lesson_time_id, day_id=day_id)
    db.session.add(add)
    db.session.commit()
    day.daily_table.append(add)
    db.session.commit()
    message = {
        "text": 'darslik qowildi',
        "color": "green"
    }
    return message


def update_old_time_table(teacher_id, day_id, lesson_time_id, room_id, subject_id, class_id, lesson_id):
    """
    darslikni yangilidigan funksiya
    :param teacher_id: teacherni id si
    :param day_id: kuni id si
    :param lesson_time_id: dars voxtini id is
    :param room_id: xonani id si
    :param subject_id: fanlani id si
    :param class_id: dinf id si
    :param lesson_id: dars id si toldirilmagan darslik bosa oshani id si keladi
    :return: darslik yangilangani xaqida xabar yuvoradi
    """
    DailyTable.query.filter(DailyTable.id == lesson_id).update({
        "room_id": room_id,
        "subject_id": subject_id,
        "teacher_id": teacher_id
    })
    db.session.commit()
    message = {
        "text": 'darslik yangilandi',
        "color": "green"
    }
    return message


def flow_student__table_information():
    """
    patok yaratilidigan page uchun objectlani yuvoradigan funksiya
    :return: tayyor listni yuvoradi
    """
    days = TimeTableDay.query.all()
    times = TimeList.query.order_by(TimeList.id).all()
    day_list = []
    for day in days:
        info = {
            "day_id": day.id,
            "day_name": day.name,
            "lessons": []
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
                filter_flow_day = DailyTable.query.filter(DailyTable.id == item.id,
                                                          DailyTable.flow_lesson == True).first()
                if filter_flow_day:
                    for lesson in info["lessons"]:
                        if lesson["time_id"] == filter_flow_day.lesson_time and filter_flow_day.day_id == info[
                            "day_id"]:
                            room = Room.query.filter(Room.id == filter_flow_day.room_id).first()
                            flow = Flow.query.filter(Flow.id == filter_flow_day.flow_id).first()
                            if filter_flow_day.lesson_time == les["time_id"]:
                                if flow and room:
                                    les.update({
                                        "status": True,
                                        "flow_name": flow.name,
                                        "flow_id": flow.id,
                                        "room_id": room.id,
                                        "room_name": room.name,
                                        "lesson_id": item.id
                                    })
                                if not flow and room:
                                    les.update({
                                        "status": True,
                                        "flow_name": None,
                                        "flow_id": None,
                                        "room_id": room.id,
                                        "room_name": room.name,
                                        "lesson_id": item.id
                                    })
                                if not room and flow:
                                    les.update({
                                        "status": True,
                                        "flow_name": flow.name,
                                        "flow_id": flow.id,
                                        "room_id": None,
                                        "room_name": None,
                                        "lesson_id": item.id
                                    })
        day_list.append(info)
    return day_list


def check_teacher_for_flow_timetable(flow_id, day_id, room_id, lesson_time_id, lesson_id):
    """
    patok yaratish uchun teacherni voxtini tekshiradi
    :param flow_id: patok id si
    :param day_id: kun id si
    :param room_id: xonani id si
    :param lesson_time_id: voxtni id si
    :param lesson_id: toldirilmagan darslik bosa uni id si
    :return: agar teacherni voxti bosa check_students_for_flow_timetable funksiyasiga yuvoradi u funksiya studentlani voxtini tekshiradi
    """
    flow = Flow.query.filter(Flow.id == flow_id).first()
    teacher = Teacher.query.filter(Teacher.id == flow.teacher_id).first()
    if teacher.daily_table:
        for daily_table in teacher.daily_table:
            if daily_table.day_id == int(day_id) and daily_table.lesson_time == int(lesson_time_id):
                if lesson_id == "":
                    message = {
                        "text": 'bu voxta darsi teacherni ',
                        "color": "red"
                    }
                    return message
                else:
                    filter_lesson = DailyTable.query.filter(DailyTable.id == lesson_id).first()
                    if filter_lesson.teacher_id == int(teacher.id):
                        return check_students_for_flow_timetable(day_id=day_id,
                                                                 lesson_time_id=lesson_time_id, room_id=room_id,
                                                                 lesson_id=lesson_id, flow_id=flow_id)
                    else:
                        message = {
                            "text": 'bu voxta darsi teacherni ',
                            "color": "red"
                        }
                        return message
            else:
                return check_students_for_flow_timetable(day_id=day_id,
                                                         lesson_time_id=lesson_time_id, room_id=room_id,
                                                         lesson_id=lesson_id, flow_id=flow_id)
    else:
        return check_students_for_flow_timetable(day_id=day_id,
                                                 lesson_time_id=lesson_time_id, room_id=room_id,
                                                 lesson_id=lesson_id, flow_id=flow_id)


def check_students_for_flow_timetable(flow_id, day_id, room_id, lesson_time_id, lesson_id):
    """
    studentlani voxtini tekshiradgan funksiya
    :param flow_id: patok id si
    :param day_id: kun id si
    :param room_id: xonani id si
    :param lesson_time_id: voxtni id si
    :param lesson_id: toldirilmagan darslik bosa uni id si
    :return: agar studentlani voxti bosa check_flow_room_timetable funksiyasiga yuvoradi u funksiya roomni voxtini tekshiradi
    """
    flow = Flow.query.filter(Flow.id == flow_id).first()
    status = True
    filter_time = TimeList.query.filter(TimeList.id == lesson_time_id).first()
    for student in flow.students:
        student_f = Student.query.filter(Student.id == student.id).first()
        for classs in student_f.classes:
            for daily_table in classs.daily_table:
                if classs.class_number <= 4:
                    if filter_time.start == "13:10":
                        message = {
                            "text": 'bu kicik sinf abedda boladi',
                            "color": "red"
                        }
                        return message
                    else:
                        if daily_table.lesson_time == int(lesson_time_id) and daily_table.day_id == int(day_id):
                            if lesson_id == "":
                                status = False
                                message = {
                                    "text": f'{classs.class_number} {classs.color} sinfi darsi bor',
                                    "color": "red"
                                }
                                return message
                            else:
                                filter_lesson = DailyTable.query.filter(DailyTable.id == lesson_id).first()
                                if filter_lesson.flow_id == int(flow_id):
                                    status = False
                                    return check_flow_room_timetable(flow_id=flow_id, day_id=day_id, room_id=room_id,
                                                                     lesson_time_id=lesson_time_id, lesson_id=lesson_id)
                                else:
                                    status = False
                                    message = {
                                        "text": f'{classs.class_number} {classs.color} sinfi darsi bor',
                                        "color": "red"
                                    }
                                    return message
                else:
                    if filter_time.start == "12:15":
                        message = {
                            "text": 'bu sinfda yuqori sinf abedda boladi',
                            "color": "red"
                        }
                        return message
                    else:
                        if daily_table.lesson_time == int(lesson_time_id) and daily_table.day_id == int(day_id):
                            if lesson_id == "":
                                status = False
                                message = {
                                    "text": f'{classs.class_number} {classs.color} sinfi darsi bor',
                                    "color": "red"
                                }
                                return message
                            else:
                                filter_lesson = DailyTable.query.filter(DailyTable.id == lesson_id).first()
                                if filter_lesson.flow_id == int(flow_id):
                                    status = False
                                    return check_flow_room_timetable(flow_id=flow_id, day_id=day_id, room_id=room_id,
                                                                     lesson_time_id=lesson_time_id, lesson_id=lesson_id)
                                else:
                                    status = False
                                    message = {
                                        "text": f'{classs.class_number} {classs.color} sinfi darsi bor',
                                        "color": "red"
                                    }
                                    return message
    if status == True:
        return check_flow_room_timetable(flow_id=flow_id, day_id=day_id, room_id=room_id,
                                         lesson_time_id=lesson_time_id, lesson_id=lesson_id)
    message = {
        "text": 'norm',
        "color": "green"
    }
    return message


def check_flow_room_timetable(flow_id, day_id, room_id, lesson_time_id, lesson_id):
    """
    bu funksiya roomni voxtini tekshiradi
    :param flow_id: patok id si
    :param day_id: kun id si
    :param room_id: xonani id si
    :param lesson_time_id: voxtni id si
    :param lesson_id: toldirilmagan darslik bosa uni id si
    :return: agar roomni voxti bosa add_flow_timetable yuvoradi yoki update_old_flow_timetable funksiyasiga yuvoriladi
    """
    room = Room.query.filter(Room.id == room_id).first()
    status = True
    if room.daily_table:
        for daily_table in room.daily_table:
            if daily_table.day_id == int(day_id) and daily_table.lesson_time == int(lesson_time_id):
                if lesson_id == "":
                    status = False
                    message = {
                        "text": 'xona zanet',
                        "color": "red"
                    }
                    return message
                else:
                    filter_lesson = DailyTable.query.filter(DailyTable.id == lesson_id).first()
                    if filter_lesson.room_id == int(room_id):
                        status = False
                        return update_old_flow_timetable(day_id=day_id,
                                                         lesson_time_id=lesson_time_id, room_id=room_id,
                                                         lesson_id=lesson_id, flow_id=flow_id)
                    else:
                        message = {
                            "text": 'bu voxtda xona zanet',
                            "color": "red"
                        }
                        status = False
                        return message
    if status == True:
        if lesson_id == "":
            return add_flow_timetable(flow_id=flow_id, day_id=day_id, room_id=room_id,
                                      lesson_time_id=lesson_time_id, lesson_id=lesson_id)
        else:
            return update_old_flow_timetable(day_id=day_id,
                                             lesson_time_id=lesson_time_id, room_id=room_id,
                                             lesson_id=lesson_id, flow_id=flow_id)
    else:
        if lesson_id == "":
            return add_flow_timetable(flow_id=flow_id, day_id=day_id, room_id=room_id,
                                      lesson_time_id=lesson_time_id, lesson_id=lesson_id)
        else:
            return update_old_flow_timetable(day_id=day_id,
                                             lesson_time_id=lesson_time_id, room_id=room_id,
                                             lesson_id=lesson_id, flow_id=flow_id)


def add_flow_timetable(flow_id, day_id, room_id, lesson_time_id, lesson_id):
    """
    patoklaga dars jadvalini saqlash uchun funksiyasi
    :param flow_id: patok id si
    :param day_id: kun id si
    :param room_id: xonani id si
    :param lesson_time_id: voxtni id si
    :param lesson_id: toldirilmagan darslik bosa uni id si
    :return: darslik saqlangani xaqida xabar jonatadi
    """
    day = TimeTableDay.query.filter(TimeTableDay.id == day_id).first()
    add = DailyTable(flow_id=flow_id, day_id=day_id, lesson_time=lesson_time_id, room_id=room_id, flow_lesson=True)
    db.session.add(add)
    db.session.commit()
    day.daily_table.append(add)
    db.session.commit()
    message = {
        "text": 'darslik qowildi',
        "color": "green"
    }
    return message


def update_old_flow_timetable(flow_id, day_id, room_id, lesson_time_id, lesson_id):
    """
    darslikni yangilash uchun funksiyasi
    :param flow_id: patok id si
    :param day_id: kun id si
    :param room_id: xonani id si
    :param lesson_time_id: voxtni id si
    :param lesson_id: toldirilmagan darslik bosa uni id si
    :return: darslikni yangilangani xaqida xabar beradi
    """
    DailyTable.query.filter(DailyTable.id == lesson_id).update({
        "room_id": room_id,
        "flow_id": flow_id
    })
    db.session.commit()
    message = {
        "text": 'darslik yangilandi',
        "color": "green"
    }
    return message


def lesson_table_list():
    """
    dars jadvalini yaratadigan pageni objectlarni yuvoradigan funksiya
    :return: tayyor malumotlani yuvoradi
    """
    lesson_list = []
    days = TimeTableDay.query.all()
    rooms = Room.query.all()
    times = TimeList.query.all()
    for day in days:
        day_info = {
            "day_name": day.name,
            "rooms": []
        }
        for room in rooms:
            room_info = {
                "room_name": room.name,
                "lessons": []
            }
            for time in times:
                les = {
                    "status": False,
                    "time_id": time.id,
                    "time_count": time.lesson_count,
                    "start": time.start,
                    "end": time.end
                }
                room_info["lessons"].append(les)
                for item in room.daily_table:
                    if item.day_id == day.id:
                        for lesson in room_info["lessons"]:
                            if lesson["time_id"] == item.lesson_time:
                                if item.lesson_time == les["time_id"]:
                                    if item.flow_lesson == True:
                                        subject = Subject.query.filter(Subject.id == item.flow.subject_id).first()
                                        teacher = Teacher.query.filter(Teacher.id == item.flow.teacher_id).first()
                                        les.update({
                                            "lesson_type": "flow",
                                            "status": True,
                                            "teacher_id": teacher.id,
                                            "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                            "subject_id": subject.id,
                                            "subject_name": subject.name,
                                            "lesson_id": item.id,
                                            "flow_name": item.flow.name,
                                            "flow_id": item.flow.id,
                                            "class_id": None
                                        })
                                    else:
                                        room = Room.query.filter(Room.id == item.room_id).first()
                                        teacher = Teacher.query.filter(Teacher.id == item.teacher_id).first()
                                        subject = Subject.query.filter(Subject.id == item.subject_id).first()
                                        if not room and subject and item.teacher_id:
                                            les.update({
                                                "lesson_type": "simple",
                                                "status": True,
                                                "teacher_id": item.teacher_id,
                                                "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                                "subject_id": item.subject_id,
                                                "subject_name": subject.name,
                                                "lesson_id": item.id,
                                                "flow_name": None,
                                                "flow_id": None,
                                                "class_id": item.class_id
                                            })
                                        if not item.teacher_id and subject and room:
                                            les.update({
                                                "lesson_type": "simple",
                                                "status": True,
                                                "room_id": item.room_id,
                                                "room_name": room.name,
                                                "teacher_id": None,
                                                "teacher_name": None,
                                                "subject_id": item.subject_id,
                                                "subject_name": subject.name,
                                                "lesson_id": item.id,
                                                "flow_name": None,
                                                "flow_id": None,
                                                "class_id": item.class_id
                                            })
                                        if not subject and room and item.teacher_id:
                                            les.update({
                                                "lesson_type": "simple",
                                                "status": True,
                                                "room_id": item.room_id,
                                                "room_name": room.name,
                                                "teacher_id": item.teacher_id,
                                                "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                                "subject_id": None,
                                                "subject_name": None,
                                                "lesson_id": item.id,
                                                "flow_name": None,
                                                "flow_id": None,
                                                "class_id": item.class_id
                                            })
                                        if not room and not item.teacher_id:
                                            les.update({
                                                "lesson_type": "simple",
                                                "status": True,
                                                "room_id": None,
                                                "room_name": None,
                                                "teacher_id": None,
                                                "teacher_name": None,
                                                "subject_id": item.subject_id,
                                                "subject_name": subject.name,
                                                "lesson_id": item.id,
                                                "flow_name": None,
                                                "flow_id": None,
                                                "class_id": item.class_id
                                            })
                                        if not room and not subject:
                                            les.update({
                                                "lesson_type": "simple",
                                                "status": True,
                                                "room_id": None,
                                                "room_name": None,
                                                "teacher_id": item.teacher_id,
                                                "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                                "subject_id": None,
                                                "subject_name": None,
                                                "lesson_id": item.id,
                                                "flow_name": None,
                                                "flow_id": None,
                                                "class_id": item.class_id
                                            })
                                        if not item.teacher_id and not subject:
                                            les.update({
                                                "lesson_type": "simple",
                                                "status": True,
                                                "room_id": item.room_id,
                                                "room_name": room.name,
                                                "teacher_id": None,
                                                "teacher_name": None,
                                                "subject_id": None,
                                                "subject_name": None,
                                                "lesson_id": item.id,
                                                "flow_name": None,
                                                "flow_id": None,
                                                "class_id": item.class_id
                                            })
                                        if item.teacher_id and subject and room:
                                            les.update({
                                                "lesson_type": "simple",
                                                "status": True,
                                                "room_id": item.room_id,
                                                "room_name": room.name,
                                                "teacher_id": item.teacher_id,
                                                "teacher_name": f'{teacher.user.name} {teacher.user.surname}',
                                                "subject_id": item.subject_id,
                                                "subject_name": subject.name,
                                                "lesson_id": item.id,
                                                "flow_name": None,
                                                "flow_id": None,
                                                "class_id": item.class_id
                                            })
            day_info["rooms"].append(room_info)
        lesson_list.append(day_info)
    return lesson_list
