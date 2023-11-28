from app import *
from backend.settings.settings import *


@app.route('/register_teacher', methods=["POST", "GET"])
def register_teacher():
    """
    teacher registratsiya qilish
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
        subject_id = request.form.get("subject_id")
        number = request.form.get("number")
        hashed = generate_password_hash(password=password, method="sha256")

        datetime_str = f'{year}-{month}-{day}'
        datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d')
        add = User(name=name, username=username, surname=surname, parent_name=parent_name, birth_date=datetime_object,
                   password=hashed, number=number)
        add.add()
        teacher = Teacher(user_id=add.id, subject_id=subject_id)
        teacher.add()
        return redirect(url_for('register'))
    return render_template("register_teacher/register_teacher.html", subjects=subjects)


@app.route('/teacher', methods=["POST", "GET"])
def teacher():
    """
    teacherlani listi
    :return:
    """
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    teachers = Teacher.query.filter(Teacher.deleted_teacher == None).all()
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
    teacher_count = Teacher.query.count()
    subjects = Subject.query.all()
    return render_template('teacher/teacher.html', teachers=teachers, user=user, news=news, jobs=jobs,
                           about_us=about_us, about_id=about_id, pages=pages, teacher_count=teacher_count,
                           subjects=subjects)


@app.route('/teacher_profile/<int:teacher_id>', methods=['POST', 'GET'])
def teacher_profile(teacher_id):
    """
    teacherni profili
    :param teacher_id: kirilgan teacherni id si
    :return:
    """
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    teacher = Teacher.query.filter(Teacher.id == teacher_id).first()
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
    return render_template('teacher_profile/teacher_profile.html', teacher=teacher, age=age, about_us=about_us,
                           news=news, jobs=jobs, about_id=about_id, user=user)


@app.route('/delete_teacher/<int:teacher_id>', methods=["POST", "GET"])
def delete_teacher(teacher_id):
    teacher = Teacher.query.filter(Teacher.id == teacher_id).first()
    add_delete_teacher = DeletedTeacher(teacher_id=teacher.id)
    add_delete_teacher.add()
    return redirect(url_for("teacher"))


@app.route('/deleted_teachers', methods=["POST", "GET"])
def deleted_teachers():
    """
    udalit qilingan teacherlani listi
    :return:
    """
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    teachers = Teacher.query.filter(Teacher.deleted_teacher).all()
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
    teaches = Teacher.query.filter(Teacher.deleted_teacher)
    pages = teaches.paginate(page=page, per_page=50)
    teacher_count = Teacher.query.count()
    subjects = Subject.query.all()
    return render_template('deleted_teachers/deleted_teachers.html', teachers=teachers, user=user, news=news, jobs=jobs,
                           about_us=about_us, about_id=about_id, pages=pages, teacher_count=teacher_count,
                           subjects=subjects)


@app.route('/return_teacher/<int:teacher_id>', methods=["POST", "GET"])
def return_teacher(teacher_id):
    DeletedTeacher.query.filter(DeletedTeacher.teacher_id == teacher_id).delete()
    db.session.commit()
    return redirect(url_for("deleted_teachers"))


@app.route('/filter_teacher', methods=["POST", "GET"])
def filter_teacher():
    """
    teavherlani filterlash
    :return:
    """

    info = request.get_json()["info"]
    filtered_teachers = []
    if info["search"] == "":
        teachers = Teacher.query.filter(Teacher.subject_id == info["subject_id"], Teacher.deleted_teacher == None).all()
        for teacher in teachers:
            birth_year = teacher.user.birth_date
            current_year = datetime.now()
            age = int(current_year.year) - int(birth_year.year)
            filtered = {
                "id": teacher.user.id,
                "username": teacher.user.username,
                "name": teacher.user.name,
                "birth_date": teacher.user.birth_date,
                "number": teacher.user.number,
                "image": teacher.user.image,
                "surname": teacher.user.surname,
                "age": age
            }
            filtered_teachers.append(filtered)
        if teachers == None:
            filtered_teachers = []
    else:
        teachers = Teacher.query.filter(Teacher.subject_id == info["subject_id"], Teacher.deleted_teacher == None).all()

        for teacher in teachers:
            users = User.query.filter(User.id == teacher.user_id, or_(User.name.like('%' + info["search"] + '%'),
                                                                      User.surname.like('%' + info["search"] + '%')))
            birth_year = teacher.user.birth_date
            current_year = datetime.now()
            age = int(current_year.year) - int(birth_year.year)
            for user in users:
                if teacher.classes:
                    filtered = {
                        "id": user.id,
                        "teacher_id": teacher.id,
                        "username": user.username,
                        "name": user.name,
                        "birth_date": user.birth_date,
                        "number": user.number,
                        "image": user.image,
                        "surname": user.surname,
                        "age": age,
                        "classes": "true"
                    }
                    filtered_teachers.append(filtered)
                else:
                    filtered = {
                        "id": user.id,
                        "teacher_id": teacher.id,
                        "username": user.username,
                        "name": user.name,
                        "birth_date": user.birth_date,
                        "number": user.number,
                        "image": user.image,
                        "surname": user.surname,
                        "age": age,
                        "classes": "false"
                    }
                    filtered_teachers.append(filtered)
        if teachers == None:
            filtered_teachers = []
    return jsonify({
        "filtered_teachers": filtered_teachers
    })


@app.route('/filter_deleted_teacher', methods=["POST", "GET"])
def filter_deleted_teacher():
    """
    teavherlani filterlash
    :return:
    """

    info = request.get_json()["info"]
    filtered_teachers = []
    if info["search"] == "":
        teachers = Teacher.query.filter(Teacher.subject_id == info["subject_id"], Teacher.deleted_teacher).all()
        for teacher in teachers:
            birth_year = teacher.user.birth_date
            current_year = datetime.now()
            age = int(current_year.year) - int(birth_year.year)
            filtered = {
                "id": teacher.user.id,
                "username": teacher.user.username,
                "name": teacher.user.name,
                "birth_date": teacher.user.birth_date,
                "number": teacher.user.number,
                "image": teacher.user.image,
                "surname": teacher.user.surname,
                "age": age
            }
            filtered_teachers.append(filtered)
        if teachers == None:
            filtered_teachers = []
    else:
        teachers = Teacher.query.filter(Teacher.subject_id == info["subject_id"], Teacher.deleted_teacher).all()

        for teacher in teachers:
            users = User.query.filter(User.id == teacher.user_id, or_(User.name.like('%' + info["search"] + '%'),
                                                                      User.surname.like('%' + info["search"] + '%')))
            birth_year = teacher.user.birth_date
            current_year = datetime.now()
            age = int(current_year.year) - int(birth_year.year)
            for user in users:
                filtered = {
                    "id": user.id,
                    "username": user.username,
                    "name": user.name,
                    "birth_date": user.birth_date,
                    "number": user.number,
                    "image": user.image,
                    "surname": user.surname,
                    "age": age
                }
                filtered_teachers.append(filtered)
        if teachers == None:
            filtered_teachers = []
    return jsonify({
        "filtered_teachers": filtered_teachers
    })


@app.route('/teacher_profile_info/<int:teacher_id>', methods=["POST", "GET"])
def teacher_profile_info(teacher_id):
    """
    teacherni profili
    :param teacher_id: kirilgan teacherni id si
    :return:
    """
    error = check_session()
    if error:
        return redirect(url_for('home'))
    teacher = Teacher.query.filter(Teacher.user_id == teacher_id).first()

    students = None
    for cl in teacher.classes:
        group = Class.query.filter(Class.id == cl.id).first()

        students = len(group.student)
    return render_template('teacher_profile_info/index.html', teacher=teacher, students=students)


@app.route('/edit_teacher_profile/<int:teacher_id>', methods=['POST', 'GET'])
def edit_teacher_profile(teacher_id):
    """
    teacher profilini ozgartirish
    :param teacher_id: kirilgan teacherni id si
    :return:
    """
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    teacher = Teacher.query.filter(Teacher.id == teacher_id).first()
    if request.method == "POST":
        if user.role == 'admin' or user.role == 'director':
            username = request.form.get("username")
            name = request.form.get("name")
            surname = request.form.get("surname")
            parent_name = request.form.get("parent_name")
            address = request.form.get("address")
            email = request.form.get("email")
            day = request.form.get("day")
            month = request.form.get("month")
            year = request.form.get("year")
            number = request.form.get("number")
            photo = request.files["photo"]

            datetime_str = f'{year}-{month}-{day}'
            datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d')
            folder = users_folder()
            if photo and checkFile(photo.filename):
                photo_file = secure_filename(photo.filename)
                photo_url = '/' + folder + photo_file
                app.config['UPLOAD_FOLDER'] = folder
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
                User.query.filter(User.id == teacher.user.id).update({
                    "name": name,
                    "username": username,
                    "surname": surname,
                    "parent_name": parent_name,
                    "number": number,
                    "birth_date": datetime_object,
                    "image": photo_url,
                    "address": address,
                    "email": email
                })
                db.session.commit()
            else:
                User.query.filter(User.id == teacher.user.id).update({
                    "name": name,
                    "username": username,
                    "surname": surname,
                    "parent_name": parent_name,
                    "number": number,
                    "birth_date": datetime_object,
                    "address": address,
                    "email": email
                })
                db.session.commit()
            return redirect(url_for("teacher_profile", teacher_id=teacher.id))
        else:
            username = request.form.get("username")
            photo = request.files["photo"]

            folder = users_folder()
            if photo and checkFile(photo.filename):
                photo_file = secure_filename(photo.filename)
                photo_url = '/' + folder + photo_file
                app.config['UPLOAD_FOLDER'] = folder
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
                User.query.filter(User.id == teacher.user.id).update({
                    "username": username,
                    "image": photo_url
                })
                db.session.commit()
            else:
                User.query.filter(User.id == teacher.user.id).update({

                    "username": username

                })
                db.session.commit()
            return redirect(url_for("teacher_profile", teacher_id=teacher.id))
    return render_template('edit_teacher_profile/edit_teacher_profile.html', user=user, teacher=teacher)


@app.route('/search_teacher', methods=["POST", "GET"])
def search_teacher():
    """
    oquvchilani qidirish
    :return:
    """
    search = request.get_json()["search"]
    users = User.query
    users = users.filter(or_(User.name.like('%' + search + '%'), User.surname.like('%' + search + '%')))
    users = users.order_by(User.name)
    filtered_users = []
    for user in users:
        if user.teacher:
            for filtered in user.teacher:
                if not filtered.deleted_teacher:
                    if filtered.classes:
                        info = {
                            "id": user.id,
                            "name": user.name,
                            "surname": user.surname,
                            "age": user.age,
                            "number": user.number,
                            "image": user.image,
                            "classes": "true"
                        }
                        filtered_users.append(info)
                    else:
                        info = {
                            "id": user.id,
                            "teacher_id": filtered.id,
                            "name": user.name,
                            "surname": user.surname,
                            "age": user.age,
                            "number": user.number,
                            "image": user.image,
                            "classes": "false"
                        }
                        filtered_users.append(info)
    return jsonify({
        "filtered_users": filtered_users
    })


@app.route('/search_deleted_teacher', methods=["POST", "GET"])
def search_deleted_teacher():
    """
    oquvchilani qidirish
    :return:
    """
    search = request.get_json()["search"]
    users = User.query
    users = users.filter(or_(User.name.like('%' + search + '%'), User.surname.like('%' + search + '%')))
    users = users.order_by(User.name)
    filtered_users = []
    for user in users:
        if user.teacher:
            for filtered in user.teacher:
                if filtered.deleted_teacher:
                    info = {
                        "id": user.id,
                        "name": user.name,
                        "surname": user.surname,
                        "age": user.age,
                        "number": user.number,
                        "image": user.image,
                    }
                    filtered_users.append(info)
    return jsonify({
        "filtered_users": filtered_users
    })
