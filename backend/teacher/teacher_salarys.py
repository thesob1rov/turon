from app import *
from backend.settings.settings import *
from datetime import datetime
import calendar


# @app.route('/teacher_salary_list', methods=["POST", "GET"])
# def teacher_salary_list():
#
#     return render_template()

@app.route('/create_teacher_salary_type', methods=["POST", "GET"])
def create_teacher_salary_type():
    if request.method == "POST":
        type = request.form.get("type")
        salary = request.form.get("salary")
        add = TeacherSalaryType(type_name=type, salary=salary)
        add.add()
        return redirect(url_for(""))
    return True


@app.route('/add_teacher_salary_percentage/<int:teacher_id>', methods=["POST", "GET"])
def add_teacher_salary_percentage(teacher_id):
    if request.method == "POST":
        salary_percentage = request.form.get("salary_percentage")
        Teacher.query.filter(Teacher.id == teacher_id).update({
            "salary_percentage": salary_percentage
        })
        db.session.commit()
        return redirect(url_for(""))
    return True


@app.route('/given_teacher_salary/<int:teacher_salary_id>', methods=["POST", "GET"])
def given_teacher_salary(teacher_salary_id):
    info = request.get_json()["info"]
    print(info)
    money = info["money"]
    reason = info["reason"]
    add = GivenSalariesInMonth(given_salary=money, reason=reason, teacher_salary_id=teacher_salary_id)
    add.add()
    teacher_salary = TeacherSalary.query.filter(TeacherSalary.id == teacher_salary_id).first()
    old_given_salary = 0
    for salary in teacher_salary.given_salaries_in_month:
        old_given_salary += int(salary.given_salary)
    calc_salary = float(teacher_salary.salary) - float(old_given_salary)
    TeacherSalary.query.filter(TeacherSalary.id == teacher_salary_id).update({
        "rest_salary": calc_salary,
        "give_salary": old_given_salary
    })
    db.session.commit()
    return jsonify({
        "name": "json"
    })


def calculate_teacher_salary():
    teachers = Teacher.query.all()
    today = datetime.today()
    date = datetime(today.year, today.month, today.day)
    calc_salary = 0
    result_calc = 0
    result = 0
    attendance_count = 0
    yy = 2017
    mm = 11
    year = Years.query.filter(Years.year == int(today.year)).first()
    month = Month.query.filter(Month.month_number == today.month, Month.years_id == year.id).first()
    cal = calendar.calendar(today.year)
    cl = calendar.Calendar()
    rez = cl.itermonthdates(today.year, 12)
    # print(calendar.calendar(today.year))
    working_days = 0
    for day in month.day:
        working_day = Day.query.filter(Day.id == day.id, Day.type_id == 1).first()
        if working_day:
            working_days += 1
    # for teacher in teachers:
    #     if teacher.daily_table:
    #         teacher_lesson_count = len(teacher.daily_table)
    #         salary_percentage = teacher.salary_percentage
    #         print(teacher_lesson_count)
    #         # ustama foizidan ciqqan summa
    #
    #         # xaftasiga dars soati / 20 * oylik
    #         calc_salary = ((teacher_lesson_count / 20) * teacher.teacher_salary_type.salary)
    #         percentage_result = (calc_salary * salary_percentage) / 100
    #         print(calc_salary)
    #         print(percentage_result)
    #         # kemagan kunlari
    #         attendance_count = TeacherAttendance.query.filter(TeacherAttendance.teacher_id == teacher.id,
    #                                                           TeacherAttendance.month_id == month.id,
    #                                                           TeacherAttendance.status == False).count()
    #         # dars bor kunlaridan kemagan kunlari ayriladi
    #         print(working_days, attendance_count)
    #         if attendance_count == 0:
    #             worked_count = working_days
    #         else:
    #             worked_count = working_days - attendance_count
    #         # oyligiga + ustama summasi
    #         overal = (calc_salary + percentage_result) * (worked_count / working_days)
    #         # ishlagan kunlari oylikdan bolib tashaladi
    #         print(worked_count)
    #         print(overal)
    #         if worked_count == 0:
    #             result = overal
    #         else:
    #             result = overal / worked_count
    #         salaries = TeacherSalary.query.filter(TeacherSalary.teacher_id == teacher.id).all()
    #         if salaries:
    #             for salary in salaries:
    #                 if salary.month_id == month.id:
    #                     TeacherSalary.query.filter(TeacherSalary.id == salary.id,
    #                                                TeacherSalary.teacher_id == teacher.id).update({
    #                         "salary": result
    #                     })
    #                     db.session.commit()
    #                 else:
    #                     add = TeacherSalary(teacher_id=teacher.id, salary=result, month_id=month.id)
    #                     add.add()
    #         else:
    #             add = TeacherSalary(teacher_id=teacher.id, salary=result, month_id=month.id)
    #             add.add()
    #     else:
    #         if teacher.teacher_attendance:
    #             attendance_count = TeacherAttendance.query.filter(TeacherAttendance.teacher_id == teacher.id,
    #                                                               TeacherAttendance.month_id == month.id,
    #                                                               TeacherAttendance.status == False).count()
    #         salaries = TeacherSalary.query.filter(TeacherSalary.teacher_id == teacher.id).all()
    #         if salaries:
    #             for salary in salaries:
    #                 if salary.month_id == month.id:
    #                     TeacherSalary.query.filter(TeacherSalary.id == salary.id,
    #                                                TeacherSalary.teacher_id == teacher.id).update({
    #                         "salary": result
    #                     })
    #                     db.session.commit()
    return "hello"
