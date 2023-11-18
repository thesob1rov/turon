from app import *
from backend.settings.settings import *
from datetime import datetime


@app.route('/worker', methods=["POST", "GET"])
def worker():
    """
    worker list
    :return:
    """
    error = check_session()
    # if error:
    #     return redirect(url_for('home'))
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
    # if error:
    #     return redirect(url_for('home'))
    user = current_user()
    worker = Worker.query.filter(Worker.id == worker_id).first()
    return render_template('worker_profile/index.html', worker=worker)


@app.route('/worker_salary/<int:worker_id>', methods=["POST", "GET"])
def worker_salary(worker_id):
    worker = Worker.query.filter(Worker.id == worker_id).first()
    salaries = WorkerSalary.query.all()
    teacher_salary_types = None
    return render_template("worker_salary/salary.html", salaries=salaries, worker=worker,
                           teacher_salary_types=teacher_salary_types)


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
        hashed = generate_password_hash(password=password, method="scrypt")

        datetime_str = f'{year}-{month}-{day}'
        datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d')
        add = User(name=name, username=username, surname=surname, parent_name=parent_name, birth_date=datetime_object,
                   password=hashed, number=number)
        add.add()
        worker =Worker(user_id=add.id,job_id=work_id)
        worker.add()
        return redirect(url_for('register'))
    return render_template("worker_register/index.html", works=works)

@app.route('/set_worker_salary', methods=["POST", "GET"])
def set_worker_salary():

    info = request.get_json()["info"]
    worker_id = info["worker_id"]
    salary = info["new_salary_money"]
    date = datetime.today()
    this_month = date.strftime("%m")
    month = Month.query.filter(Month.month_number == this_month).first()
    print(month)
    add = WorkerSalary(worker_id=worker_id, salary=salary, month_id=month.id)
    add.add()
    Worker.query.filter(Worker.id == worker_id).update({
        "salary": salary
    })
    db.session.commit()
    return jsonify()
