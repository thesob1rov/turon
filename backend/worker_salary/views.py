from app import *
from backend.settings.settings import *
from datetime import datetime


def get_worker_salary():
    """
    har oy workerlaga oylik yaratib beradi oyligiga qarab worker routega otganda avto yaratib quyadi
    :return:
    """
    today = datetime.today()
    year = Years.query.filter(Years.year == today.year).first()
    month = Month.query.filter(Month.month_number == today.month, Month.years_id == year.id).first()
    workers = Worker.query.all()
    for worker in workers:
        if worker.salary:
            worker_salary = WorkerSalary.query.filter(WorkerSalary.worker_id == worker.id,
                                                      WorkerSalary.month_id == month.id).first()
            if not worker_salary:
                add = WorkerSalary(worker_id=worker.id, salary=worker.salary, month_id=month.id)
                add.add()


@app.route('/worker', methods=["POST", "GET"])
def worker():
    """
    worker list
    :return:
    """
    get_worker_salary()
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    workers = Worker.query.all()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    if about_us:
        about_id = about_us.id
    page = request.args.get('page')
    students = Student.query
    pages = students.paginate(page=page, per_page=50)
    # teacher_count = Teacher.query.count()
    subjects = Subject.query.all()
    return render_template('worker_salary/index.html', workers=workers, user=user, news=news, jobs=jobs,
                           about_us=about_us, about_id=about_id, pages=pages,
                           subjects=subjects)


@app.route('/worker_profile/<int:worker_id>', methods=['POST', 'GET'])
def worker_profile(worker_id):
    """
    worker profili
    :param teacher_id: kirilgan teacherni id si
    :return:
    """
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    worker = Worker.query.filter(Worker.id == worker_id).first()
    return render_template('worker_profile/index.html', worker=worker)


@app.route('/worker_salary/<int:worker_id>', methods=["POST", "GET"])
def worker_salary(worker_id):
    worker = Worker.query.filter(Worker.id == worker_id).first()
    salaries = WorkerSalary.query.filter(WorkerSalary.worker_id == worker_id).order_by(WorkerSalary.id).all()
    return render_template("worker_salary/salary.html", salaries=salaries, worker=worker)


@app.route('/worker_salaries_in_month/<int:worker_salary_id>', methods=["POST", "GET"])
def worker_salaries_in_month(worker_salary_id):
    worker_salary = WorkerSalary.query.filter(WorkerSalary.id == worker_salary_id).first()
    worker_salary_inDay_all = WorkerSalaryInDay.query.filter(
        WorkerSalaryInDay.worker_salary_id == worker_salary.id,
        WorkerSalaryInDay.deleted_worker_salary_inDay == None).order_by(
        WorkerSalaryInDay.id).all()
    account_types = AccountType.query.all()
    return render_template("worker_salary/add.html", worker_salary=worker_salary,
                           worker_salary_inDay_all=worker_salary_inDay_all,
                           account_types=account_types)


@app.route('/change_worker_salary_account_type', methods=["POST"])
def change_worker_salary_account_type():
    info = request.get_json()["info"]
    worker_salary_inDay_id = info["worker_salary_inDay_id"]
    account_type_id = info["account_type_id"]
    WorkerSalaryInDay.query.filter(WorkerSalaryInDay.id == worker_salary_inDay_id).update({
        'account_type_id': account_type_id
    })
    db.session.commit()
    return jsonify()


@app.route('/given_worker_salary', methods=["POST", "GET"])
def given_worker_salary():
    info = request.get_json()["info"]
    worker_salary_id = info["worker_salary_id"]
    account_type_id = info["account_type_id"]
    money = info["money"]
    reason = info["reason"]
    today = datetime.today()
    year = Years.query.filter(Years.year == int(today.year)).first()
    month = Month.query.filter(Month.month_number == today.month, Month.years_id == year.id).first()
    day = Day.query.filter(Day.year_id == year.id, Day.month_id == month.id, Day.day_number == int(today.day)).first()

    add = WorkerSalaryInDay(salary=money, reason=reason, worker_salary_id=worker_salary_id,
                            account_type_id=account_type_id, day_id=day.id, year_id=year.id, month_id=month.id)
    add.add()
    worker_salary = WorkerSalary.query.filter(WorkerSalary.id == worker_salary_id).first()
    old_given_salary = 0
    for salary in worker_salary.worker_salary_in_days:
        check = WorkerSalaryInDay.query.filter(WorkerSalaryInDay.id == salary.id,
                                               WorkerSalaryInDay.deleted_worker_salary_inDay == None).order_by(
            WorkerSalaryInDay.id).first()
        if check:
            old_given_salary += int(salary.salary)
            calc_salary = float(worker_salary.salary) - float(old_given_salary)
            WorkerSalary.query.filter(WorkerSalary.id == worker_salary_id).update({
                "rest_salary": round(calc_salary),
                "give_salary": old_given_salary
            })
            db.session.commit()

    return jsonify()


@app.route('/register_worker', methods=["POST", "GET"])
def register_worker():
    """
    worker registratsiya qilish
    :return:
    """
    error = check_session()
    if error:
        return redirect(url_for('home'))
    works = Job.query.all()
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        surname = request.form.get("surname")
        parent_name = request.form.get("parent_name")
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")
        password = request.form.get("password")
        work_id = request.form.get("work_id")
        number = request.form.get("number")
        hashed = generate_password_hash(password=password)

        datetime_str = f'{year}-{month}-{day}'
        datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d')
        add = User(name=name, username=username, surname=surname, parent_name=parent_name, birth_date=datetime_object,
                   password=hashed, number=number)
        add.add()
        worker = Worker(user_id=add.id, job_id=work_id)
        worker.add()
        return redirect(url_for('register'))
    return render_template("worker_register/index.html", works=works)


@app.route('/set_worker_salary', methods=["POST", "GET"])
def set_worker_salary():
    '''
    workerga oylik belgilash yoki oylik qiymatini uzgartirish
    :return:
    '''
    info = request.get_json()["info"]
    worker_id = info["worker_id"]
    salary = info["new_salary_money"]
    Worker.query.filter(Worker.id == worker_id).update({
        "salary": salary
    })
    db.session.commit()
    return jsonify()


@app.route('/delete_worker_given_salary', methods=["POST", "GET"])
def delete_worker_given_salary():
    info = request.get_json()["info"]
    given_salary_id = info["given_salary_id"]
    today = datetime.today()
    date = datetime(today.year, today.month, today.day)
    deletes = WorkerSalaryInDay.query.filter(WorkerSalaryInDay.id == int(given_salary_id)).first()
    worker_salary = WorkerSalary.query.filter(WorkerSalary.id == deletes.worker_salary_id).first()
    old_deleted_salary = int(worker_salary.give_salary)
    rest_deleted_salary = int(worker_salary.rest_salary)
    check = WorkerSalaryInDay.query.filter(WorkerSalaryInDay.id == int(given_salary_id),
                                           WorkerSalaryInDay.deleted_worker_salary_inDay == None).order_by(
        WorkerSalaryInDay.id).first()
    if check:
        old_deleted_salary -= int(check.salary)
        calc_salary = float(check.salary) + float(rest_deleted_salary)
        WorkerSalary.query.filter(WorkerSalary.id == deletes.worker_salary_id).update({
            "rest_salary": round(calc_salary),
            "give_salary": old_deleted_salary
        })
    salary_worker = DeletedWorkerSalaryInDay(worker_salary_in_day_id=int(given_salary_id), date=date)
    salary_worker.add()
    return jsonify()
