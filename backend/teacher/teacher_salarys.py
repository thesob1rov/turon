from app import *
from backend.settings.settings import *
from datetime import datetime
import calendar


@app.route('/teacher_salary/<int:teacher_id>', methods=["POST", "GET"])
def teacher_salary(teacher_id):
    teacher = Teacher.query.filter(Teacher.id == teacher_id).first()
    salaries = TeacherSalary.query.filter(TeacherSalary.teacher_id == teacher.id).all()
    teacher_salary_types = TeacherSalaryType.query.all()
    return render_template("teacher_salary/oylik.html", salaries=salaries, teacher=teacher,
                           teacher_salary_types=teacher_salary_types)


@app.route('/enter_teacher_salary_type', methods=["POST", "GET"])
def enter_teacher_salary_type():
    info = request.get_json()["info"]
    teacher_id = info["teacher_id"]
    salary_type_id = info["salary_type_id"]
    Teacher.query.filter(Teacher.id == teacher_id).update({
        "salary_type": salary_type_id
    })
    db.session.commit()
    calculate_teacher_salary()
    return jsonify()


@app.route('/create_teacher_salary_type', methods=["POST", "GET"])
def create_teacher_salary_type():
    info = request.get_json()["info"]
    teacher_id = info["teacher_id"]
    type_name = info["salary_type_name"]
    salary = info["new_salary_money"]
    add = TeacherSalaryType(type_name=type_name, salary=salary)
    add.add()
    Teacher.query.filter(Teacher.id == teacher_id).update({
        "salary_type": add.id
    })
    db.session.commit()
    calculate_teacher_salary()
    return jsonify()


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


@app.route('/given_teacher_salary', methods=["POST", "GET"])
def given_teacher_salary():
    info = request.get_json()["info"]
    teacher_salary_id = info["teacher_salary_id"]
    account_type_id = info["account_type_id"]
    money = info["money"]
    reason = info["reason"]

    today = datetime.today()
    year = Years.query.filter(Years.year == int(today.year)).first()
    month = Month.query.filter(Month.month_number == today.month, Month.years_id == year.id).first()
    day = Day.query.filter(Day.year_id == year.id, Day.month_id == month.id, Day.day_number == int(today.day)).first()
    add = GivenSalariesInMonth(given_salary=money, reason=reason, teacher_salary_id=teacher_salary_id, day_id=day.id,
                               account_type_id=account_type_id, year_id=year.id, month_id=month.id)
    add.add()
    teacher_salary = TeacherSalary.query.filter(TeacherSalary.id == teacher_salary_id).first()
    old_given_salary = 0
    for salary in teacher_salary.given_salaries_in_month:
        old_given_salary += int(salary.given_salary)
    calc_salary = float(teacher_salary.salary) - float(old_given_salary)
    TeacherSalary.query.filter(TeacherSalary.id == teacher_salary_id).update({
        "rest_salary": round(calc_salary),
        "give_salary": old_given_salary
    })
    db.session.commit()
    return jsonify()


@app.route('/delete_teacher_given_salary', methods=["POST", "GET"])
def delete_teacher_given_salary():
    info = request.get_json()["info"]
    print(info)
    given_salary_id = info["given_salary_id"]

    GivenSalariesInMonth.query.filter(GivenSalariesInMonth.id == int(given_salary_id)).delete()
    db.session.commit()
    return jsonify()


@app.route('/teacher_salaries_in_month/<int:teacher_salary_id>', methods=["POST", "GET"])
def teacher_salaries_in_month(teacher_salary_id):
    teacher_salary = TeacherSalary.query.filter(TeacherSalary.id == teacher_salary_id).first()
    account_types = AccountType.query.all()
    return render_template("given_teacher_salary/salary.html", teacher_salary=teacher_salary,
                           account_types=account_types)


@app.route('/enter_teacher_worked_days', methods=["POST", "GET"])
def enter_teacher_worked_days():
    info = request.get_json()["info"]
    teacher_salary_id = info["teacher_salary_id"]
    worked_days = info["worked_days"]
    print(teacher_salary_id, worked_days)
    TeacherSalary.query.filter(TeacherSalary.id == teacher_salary_id).update({
        "worked_days": worked_days
    })
    db.session.commit()
    calculate_teacher_salary()
    return jsonify()


def calculate_teacher_salary():
    teachers = Teacher.query.all()
    today = datetime.today()
    calc_salary = 0
    result_calc = 0
    year = Years.query.filter(Years.year == int(today.year)).first()
    month = Month.query.filter(Month.month_number == today.month, Month.years_id == year.id).first()
    overal = 0
    working_days = 0
    for day in month.day:
        working_day = Day.query.filter(Day.id == day.id, Day.type_id == 1).first()
        if working_day:
            working_days += 1
    for teacher in teachers:
        if teacher.daily_table:
            teacher_lesson_count = len(teacher.daily_table)
            salary_percentage = teacher.salary_percentage
            calc_salary = ((teacher_lesson_count / 20) * teacher.teacher_salary_type.salary)
            percentage_result = (calc_salary * salary_percentage) / 100
            salary = TeacherSalary.query.filter(TeacherSalary.teacher_id == teacher.id,
                                                TeacherSalary.month_id == month.id).first()
            if salary:
                if salary.worked_days:
                    overal = (calc_salary + percentage_result) * (int(salary.worked_days) / working_days)
                    TeacherSalary.query.filter(TeacherSalary.teacher_id == teacher.id,
                                               TeacherSalary.month_id == month.id).update({
                        "salary": round(overal)
                    })
                    db.session.commit()
                else:
                    overal = (calc_salary + percentage_result)
                    TeacherSalary.query.filter(TeacherSalary.teacher_id == teacher.id,
                                               TeacherSalary.month_id == month.id).update({
                        "salary": round(overal)
                    })
                    db.session.commit()
            else:
                add = TeacherSalary(teacher_id=teacher.id, salary=overal, month_id=month.id)
                add.add()
        else:
            TeacherSalary.query.filter(TeacherSalary.teacher_id == teacher.id,
                                       TeacherSalary.month_id == month.id).update({
                "salary": overal
            })
            db.session.commit()
    return "hello"
