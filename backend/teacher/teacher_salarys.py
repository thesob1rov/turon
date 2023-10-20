from app import *
from backend.settings.settings import *


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


@app.route('/calculate_teacher_salary', methods=["POST", "GET"])
def calculate_teacher_salary():
    teachers = Teacher.query.all()
    for teacher in teachers:
        if teacher.daily_table:
            teacher_lesson_count = len(teacher.daily_table)
            salary_percentage = teacher.salary_percentage
            percentage_result = (teacher.teacher_salary_type.salary * salary_percentage) / 100
            print(percentage_result)
            calc_salary = ((teacher_lesson_count / 20) * teacher.teacher_salary_type.salary) + percentage_result
            print(
                f'{teacher.user.name} {teacher.user.surname} {teacher_lesson_count} {teacher.teacher_salary_type.salary} oyligi {calc_salary}')
    return "hello"
