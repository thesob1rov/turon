from app import *
from backend.settings.settings import *


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
    if error:
        return redirect(url_for('home'))
    user = current_user()
    # teacher = Teacher.query.filter(Teacher.id == teacher_id).first()
    teacher_birth_year = teacher.user.birth_date
    current_year = datetime.now()

    age = int(current_year.year) - int(teacher_birth_year.year)
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    if about_us:
        about_id = about_us.id
    return render_template('worker_profile/index.html', teacher=teacher, age=age, about_us=about_us,
                           news=news, jobs=jobs, about_id=about_id, user=user)


@app.route('/register_worker', methods=["POST", "GET"])
def register_worker():
    """
    worker registratsiya qilish
    :return:
    """
    error = check_session()
    if error:
        return redirect(url_for('home'))
    subjects = Subject.query.all()
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        surname = request.form.get("surname")
        parent_name = request.form.get("parent_name")
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")
        password = request.form.get("password")
        # work_id = request.form.get("work_id")
        number = request.form.get("number")
        hashed = generate_password_hash(password=password, method="sha256")

        datetime_str = f'{year}-{month}-{day}'
        datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d')
        add = User(name=name, username=username, surname=surname, parent_name=parent_name, birth_date=datetime_object,
                   password=hashed, number=number)
        add.add()
        worker = Worker(user_id=add.id)
        worker.add()
        return redirect(url_for('register'))
    return render_template("worker_register/index.html", subjects=subjects)
