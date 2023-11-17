from app import *
from datetime import datetime
from backend.settings.settings import *


@app.route('/lesson_plan/<int:teacher_id>', methods=['POST', 'GET'])
def lesson_plan(teacher_id):
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = User.query.filter(User.id == teacher_id).first()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    time_list = TimeList.query.order_by(TimeList.id).all()
    if about:
        about_id = about.id
    if about_us:
        about_id = about_us.id
    day_list = filter_day_lesson(teacher_id)
    return render_template('lesson_plan/index.html', day_list=day_list, user=user, about_us=about_us, news=news,
                           jobs=jobs,
                           about=about, about_id=about_id, time_list=time_list)


@app.route('/add_lesson_plan', methods=['POST'])
def add_lesson_plan():
    user = current_user()
    teacher = Teacher.query.filter(Teacher.user_id == user.id).first()
    day_id = request.get_json()["day_id"]
    lesson_time_id = request.get_json()["lesson_time_id"]
    name = request.get_json()["name"]
    target = request.get_json()["target"]
    main = request.get_json()["main"]
    assessment = request.get_json()["assessment"]
    homework = request.get_json()["homework"]
    lesson_plan = Lesson_plan_day(name=name, target=target, main=main, assessment=assessment, homework=homework,
                                  day_id=day_id, lesson_time_id=lesson_time_id, teacher_id=teacher.id)
    lesson_plan.add()

    return jsonify()


@app.route('/change_lesson_plan', methods=['POST'])
def change_lesson_plan():
    day_id = request.get_json()["day_id"]
    lesson_time_id = request.get_json()["lesson_time_id"]
    name = request.get_json()["name"]
    target = request.get_json()["target"]
    main = request.get_json()["main"]
    assessment = request.get_json()["assessment"]
    homework = request.get_json()["homework"]
    Lesson_plan_day.query.filter(Lesson_plan_day.day_id == day_id,
                                 Lesson_plan_day.lesson_time_id == lesson_time_id).update({
        'name': name,
        'target': target,
        'main': main,
        'assessment': assessment,
        'homework': homework
    })
    db.session.commit()
    return jsonify()


@app.route('/get_lesson_plan', methods=['POST'])
def get_lesson_plan():
    day_id = request.get_json()["day_id"]
    lesson_time_id = request.get_json()["lesson_time_id"]
    lesson_plan = Lesson_plan_day.query.filter(Lesson_plan_day.day_id == day_id,
                                               Lesson_plan_day.lesson_time_id == lesson_time_id).first()
    if lesson_plan:
        lesson_data = {
            'name': lesson_plan.name,
            'target': lesson_plan.target,
            'assessment': lesson_plan.assessment,
            'main': lesson_plan.main,
            'homework': lesson_plan.homework,
            'status': True
        }
    else:
        lesson_data = {
            'status': False
        }
    return jsonify({
        'lesson_data': lesson_data
    })


def filter_day_lesson(teacher_id):
    date = datetime.today()
    today = date.strftime("%d")
    this_month = date.strftime("%m")
    this_year = date.strftime("%Y")

    year_this = Years.query.filter(Years.year == this_year).first()
    month_this = Month.query.filter(Month.month_number == this_month).first()
    day_in_month = Day.query.filter(Day.month_id == month_this.id, Day.year_id == year_this.id).order_by(Day.id).all()
    day_list = []
    day_table = [
        {
            'id': 1,
            'name': 'Monday'
        }, {
            'id': 2,
            'name': 'Tuesday'
        }, {
            'id': 3,
            'name': 'Wednesday'
        }, {
            'id': 4,
            'name': 'Thursday'
        }, {
            'id': 5,
            'name': 'Friday'
        }, {
            'id': 6,
            'name': 'Saturday'
        }, {
            'id': 7,
            'name': 'Sunday'
        }
    ]
    for day in day_in_month:
        day_lesson_id = None
        for days in day_table:
            if days['name'] == day.day_name:
                day_lesson_id = days['id']
        day_lesson_all = DailyTable.query.filter(DailyTable.day_id == day_lesson_id).order_by(DailyTable.id).all()
        time_list = TimeList.query.order_by(TimeList.id).all()
        day_lessons = []

        if day_lesson_all:
            for time in time_list:
                info_day = {
                    'status': False,
                    'time_id': None,
                    'lesson_status': None

                }
                for day_lesson in day_lesson_all:
                    if day_lesson.lesson_time == time.id:
                        lesson_plan = Lesson_plan_day.query.filter(Lesson_plan_day.day_id == day.id,
                                                                   Lesson_plan_day.lesson_time_id == time.id).first()
                        if lesson_plan:
                            lesson_status = True
                        else:
                            lesson_status = False

                        info_day['status'] = True
                        info_day['time_id'] = day_lesson.lesson_time
                        info_day['lesson_status'] = lesson_status
                if info_day['status']:
                    info = {
                        'name': 'Sinf',
                        'time_id': info_day['time_id'],
                        'lesson_status': info_day['lesson_status']
                    }
                    day_lessons.append(info)
                else:
                    info = {
                        'name': None
                    }
                    day_lessons.append(info)
        else:
            for time in time_list:
                info = {
                    'name': None
                }
                day_lessons.append(info)
        day_change_status = False
        if int(day.years.year) >= int(this_year):
            if int(day.month.month_number) >= int(this_month):
                if int(day.day_number) >= int(today):
                    day_change_status = True

        day_object = {
            'day_id': day.id,
            'day_number': day.day_number,
            'day_name': day.day_name,
            'day_lessons': day_lessons,
            'day_change_status': day_change_status
        }
        day_list.append(day_object)
    return day_list
