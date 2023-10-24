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
    print(date)
    calc_salary = 0
    yy = 2017
    mm = 11
    cal = calendar.calendar(today.year)
    cl = calendar.Calendar()
    rez = cl.itermonthdates(today.year, 12)
    # print(calendar.calendar(today.year))
    print(list(rez.datetime))
    for teacher in teachers:
        if teacher.daily_table:
            teacher_lesson_count = len(teacher.daily_table)
            salary_percentage = teacher.salary_percentage
            percentage_result = (teacher.teacher_salary_type.salary * salary_percentage) / 100
            print(percentage_result)
            calc_salary = ((teacher_lesson_count / 20) * teacher.teacher_salary_type.salary) + percentage_result
            salaries = TeacherSalary.query.filter(TeacherSalary.teacher_id == teacher.id).all()
            if salaries:
                for salary in salaries:
                    if salary.date.strftime("%Y") == str(today.year) and salary.date.strftime("%m") == str(today.month):
                        TeacherSalary.query.filter(TeacherSalary.id == salary.id,
                                                   TeacherSalary.teacher_id == teacher.id).update({
                            "salary": calc_salary
                        })
                        db.session.commit()
                        print("bu yil bor")
                    else:
                        add = TeacherSalary(teacher_id=teacher.id, salary=calc_salary, date=date)
                        add.add()
            else:
                add = TeacherSalary(teacher_id=teacher.id, salary=calc_salary, date=date)
                add.add()
            print(
                f'{teacher.user.name} {teacher.user.surname} {teacher_lesson_count} {teacher.teacher_salary_type.salary} '
                f' salary {calc_salary}')
        else:
            salaries = TeacherSalary.query.filter(TeacherSalary.teacher_id == teacher.id).all()
            if salaries:
                for salary in salaries:
                    if salary.date.strftime("%Y") == str(today.year) and salary.date.strftime("%m") == str(today.month):
                        TeacherSalary.query.filter(TeacherSalary.id == salary.id,
                                                   TeacherSalary.teacher_id == teacher.id).update({
                            "salary": calc_salary
                        })
                        db.session.commit()
    return "hello"
