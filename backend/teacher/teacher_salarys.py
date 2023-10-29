from app import *
from backend.settings.settings import *
from datetime import datetime
import calendar


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


def calculate_teacher_salary():
    teachers = Teacher.query.all()
    today = datetime.today()
    date = datetime(today.year, today.month, today.day)
    calc_salary = 0
    result_calc = 0
    yy = 2017
    mm = 11
    year = Years.query.filter(Years.year == int(today.year)).first()
    month = Month.query.filter(Month.month_number == today.month, Month.years_id == year.id).first()
    cal = calendar.calendar(today.year)
    cl = calendar.Calendar()
    rez = cl.itermonthdates(today.year, 12)
    # print(calendar.calendar(today.year))
    for teacher in teachers:
        if teacher.daily_table:
            teacher_lesson_count = len(teacher.daily_table)
            salary_percentage = teacher.salary_percentage
            percentage_result = (teacher.teacher_salary_type.salary * salary_percentage) / 100
            calc_salary = ((teacher_lesson_count / 20) * teacher.teacher_salary_type.salary)
            result_calc = (calc_salary * salary_percentage) / 100
            salaries = TeacherSalary.query.filter(TeacherSalary.teacher_id == teacher.id).all()

            for attendance in teacher.teacher_attendance:
                attendance_count = TeacherAttendance.query.filter(TeacherAttendance.teacher_id == attendance.teacher_id,
                                                                  TeacherAttendance.month_id == attendance.month_id,
                                                                  TeacherAttendance.status == True).all()
                print(attendance_count)
            if salaries:
                for salary in salaries:
                    if salary.month_id == month.id:
                        TeacherSalary.query.filter(TeacherSalary.id == salary.id,
                                                   TeacherSalary.teacher_id == teacher.id).update({
                            "salary": calc_salary
                        })
                        db.session.commit()
                    else:
                        add = TeacherSalary(teacher_id=teacher.id, salary=result_calc, month_id=month.id)
                        add.add()
            else:
                add = TeacherSalary(teacher_id=teacher.id, salary=result_calc, month_id=month.id)
                add.add()
        else:
            if teacher.teacher_attendance:

                for attendance in teacher.teacher_attendance:
                    attendance_count = TeacherAttendance.query.filter(TeacherAttendance.teacher_id == attendance.teacher_id,
                                                                      TeacherAttendance.month_id == attendance.month_id,
                                                                      TeacherAttendance.status == True).count()
                    print(attendance_count)
            salaries = TeacherSalary.query.filter(TeacherSalary.teacher_id == teacher.id).all()
            if salaries:
                for salary in salaries:
                    if salary.month_id == month.id:
                        TeacherSalary.query.filter(TeacherSalary.id == salary.id,
                                                   TeacherSalary.teacher_id == teacher.id).update({
                            "salary": result_calc
                        })
                        db.session.commit()
    return "hello"
