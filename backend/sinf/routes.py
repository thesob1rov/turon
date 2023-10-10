from app import *
from backend.settings.settings import *
from backend.student import *
import datetime


@app.route('/classes', methods=["POST", "GET"])
def classes():
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    filter_info = []
    if about_us:
        about_id = about_us.id
    teachers = Teacher.query.all()
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    students = Class.query.filter(Class.deleted_classes == None)
    pages = students.paginate(page=page, per_page=50)
    student_count = Class.query.count()
    languages = LanguageType.query.all()
    return render_template('classes/classes.html', user=user, about_us=about_us, about_id=about_id, teachers=teachers,
                           page=page, pages=pages, news=news, jobs=jobs, student_count=student_count,
                           languages=languages)


@app.route('/filter_classes', methods=["POST", "GET"])
def filter_classes():
    info = request.get_json()["info"]
    filter_classes = []
    if info['language_type'] == "all":
        if info['class_number'] == 'sinflar':
            classes = Class.query.filter(Class.deleted_classes == None).all()
            for group in classes:
                if info['color'] == "all":
                    filtered = {
                        "id": group.id,
                        "name": group.name,
                        "teacher": group.teacher[0].user.name,
                        "student_number": len(group.student),
                        "class_number": group.class_number,
                        "color": group.color,
                        "language": group.language.name
                    }
                    filter_classes.append(filtered)
                if info['color'] == group.color:
                    filtered = {
                        "id": group.id,
                        "name": group.name,
                        "teacher": group.teacher[0].user.name,
                        "student_number": len(group.student),
                        "class_number": group.class_number,
                        "color": group.color,
                        "language": group.language.name
                    }
                    filter_classes.append(filtered)
        else:
            classes = Class.query.filter(Class.class_number == info['class_number'],
                                         Class.deleted_classes == None).all()
            for group in classes:
                if info['color'] == "all":
                    filtered = {
                        "id": group.id,
                        "name": group.name,
                        "teacher": group.teacher[0].user.name,
                        "student_number": len(group.student),
                        "class_number": group.class_number,
                        "color": group.color,
                        "language": group.language.name
                    }
                    filter_classes.append(filtered)
                if info['color'] == group.color:
                    filtered = {
                        "id": group.id,
                        "name": group.name,
                        "teacher": group.teacher[0].user.name,
                        "student_number": len(group.student),
                        "class_number": group.class_number,
                        "color": group.color,
                        "language": group.language.name
                    }
                    filter_classes.append(filtered)
        print(filter_classes)
    else:
        if info['class_number'] == 'sinflar':
            classes = Class.query.filter(Class.language_type == info['language_type'],
                                         Class.deleted_classes == None).all()
            for group in classes:
                if info['color'] == "all":
                    filtered = {
                        "id": group.id,
                        "name": group.name,
                        "teacher": group.teacher[0].user.name,
                        "student_number": len(group.student),
                        "class_number": group.class_number,
                        "color": group.color,
                        "language": group.language.name
                    }
                    filter_classes.append(filtered)
                if info['color'] == group.color:
                    filtered = {
                        "id": group.id,
                        "name": group.name,
                        "teacher": group.teacher[0].user.name,
                        "student_number": len(group.student),
                        "class_number": group.class_number,
                        "color": group.color,
                        "language": group.language.name
                    }
                    filter_classes.append(filtered)
        else:
            classes = Class.query.filter(Class.class_number == info['class_number'],
                                         Class.language_type == info['language_type'],
                                         Class.deleted_classes == None).all()
            for group in classes:
                if info['color'] == "all":
                    filtered = {
                        "id": group.id,
                        "name": group.name,
                        "teacher": group.teacher[0].user.name,
                        "student_number": len(group.student),
                        "class_number": group.class_number,
                        "color": group.color,
                        "language": group.language.name
                    }
                    filter_classes.append(filtered)
                if info['color'] == group.color:
                    filtered = {
                        "id": group.id,
                        "name": group.name,
                        "teacher": group.teacher[0].user.name,
                        "student_number": len(group.student),
                        "class_number": group.class_number,
                        "color": group.color,
                        "language": group.language.name
                    }
                    filter_classes.append(filtered)
        print(filter_classes)
    return jsonify({
        "filter_classes": filter_classes
    })


@app.route('/creat_class', methods=["POST", "GET"])
def creat_class():
    class_info = request.get_json()['class_info']
    class_name = class_info['name']
    class_number = class_info['class_number']
    class_color = class_info['color']
    language_type = class_info['creat_language_type']
    add_class = Class(name=class_name, class_number=class_number, color=class_color,
                      language_type=language_type)
    add_class.add()
    teacher_id = class_info['teacher_id']
    filter_teacher = Teacher.query.filter(Teacher.id == teacher_id).first()
    if not filter_teacher.classes:
        filter_teacher.classes.append(add_class)
        db.session.commit()
    else:
        print('bu teacherni classi bor')
    students = class_info['students']
    for student in students:
        print(student)
        filter_student = Student.query.filter(Student.user_id == int(student)).first()
        if not filter_student.classes:
            filter_student.classes.append(add_class)
            db.session.commit()
        else:
            print('bu studentni classi bor ')
    print(class_name)
    return jsonify()


@app.route('/class_profile/<int:class_id>', methods=["POST", "GET"])
def class_profile(class_id):
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    classs = Class.query.filter(Class.id == class_id).first()
    students = len(classs.student)
    teachers = Teacher.query.filter(Teacher.classes == None).all()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    classes = Class.query.all()
    class_types = ClassType.query.order_by(ClassType.id).all()
    return render_template('class_profile/sinf.html', news=news, about_id=about_id, about_us=about_us,
                           classs=classs, students=students, teachers=teachers, user=user, jobs=jobs, about=about,
                           classes=classes, class_types=class_types)


@app.route('/edit_class/<int:class_id>', methods=["POST", "GET"])
def edit_class(class_id):
    error = check_session()
    if error:
        return redirect(url_for('home'))
    group = Class.query.filter(Class.id == class_id).first()
    if request.method == "POST":
        name = request.form.get("name")
        teacher_id = request.form.get("teacher")
        color = request.form.get("color")
        class_number = request.form.get("class_number")
        Class.query.filter(Class.id == class_id).update({
            "name": name,
            "color": color,
            "class_number": class_number
        })
        db.session.commit()
        if teacher_id:
            new_teach = Teacher.query.filter(Teacher.id == teacher_id).first()
            if group.teacher:
                old_teacher = None
                for teach in group.teacher:
                    old_teacher = teach
                filter_teach = Teacher.query.filter(Teacher.id == old_teacher.id).first()
                if not new_teach.classes:
                    group.teacher.remove(filter_teach)
                    db.session.commit()
                    group.teacher.append(new_teach)
                    db.session.commit()
            else:
                group.teacher.append(new_teach)
                db.session.commit()

    return redirect(url_for("class_profile", class_id=group.id))


@app.route('/delete_student_in_class', methods=["POST"])
def delete_student_in_class():
    info = request.get_json()["info"]
    if info["delete_type"] == "in_class":
        group = Class.query.filter(Class.id == info['class_id']).first()
        student = Student.query.filter(Student.id == info['student_id']).first()
        student.classes.remove(group)
        db.session.commit()
        add = DeletedStudentForClasses(student_id=info['student_id'], class_id=info['class_id'], reason=info['reason'])
        db.session.add(add)
        db.session.commit()
        print("in_class")
    else:
        group = Class.query.filter(Class.id == info['class_id']).first()
        student = Student.query.filter(Student.id == info['student_id']).first()
        student.classes.remove(group)
        db.session.commit()
        add_delete_student = DeletedStudent(student_id=info['student_id'])
        db.session.add(add_delete_student)
        db.session.commit()
        add = DeletedStudentForClasses(student_id=info['student_id'], class_id=info['class_id'], reason=info['reason'])
        db.session.add(add)
        db.session.commit()
        print("all")
    print(info['class_id'])
    return jsonify()


@app.route('/transfer_students_in_class', methods=["POST", "GET"])
def transfer_students_in_class():
    info = request.get_json()["info_class"]
    print(info)
    for student_id in info["students"]:
        student = Student.query.filter(Student.id == student_id).first()
        old_class = None
        for classs in student.classes:
            old_class = classs
        new_class = Class.query.filter(Class.id == info["class_id"]).first()
        student.classes.remove(old_class)
        db.session.commit()
        student.classes.append(new_class)
        db.session.commit()
    return jsonify()


@app.route('/delete_class', methods=["POST", "GET"])
def delete_class():
    info = request.get_json()["info"]
    group = Class.query.filter(Class.id == info['class_id']).first()
    if group.student:
        if info["delete_type"] == "in_class":
            for student in group.student:
                student.classes.remove(group)
                db.session.commit()
                add = DeletedStudentForClasses(student_id=student.id, class_id=group.id, reason=info['reason'])
                db.session.add(add)
                db.session.commit()
                del_class = DeletedClasses(class_id=group.id)
                db.session.add(del_class)
                db.session.commit()
                print("in_class")
        else:
            for student in group.student:
                student.classes.remove(group)
                db.session.commit()
                add_delete_student = DeletedStudent(student_id=student.id)
                db.session.add(add_delete_student)
                db.session.commit()
                add = DeletedStudentForClasses(student_id=student.id, class_id=group.id, reason=info['reason'])
                db.session.add(add)
                db.session.commit()
                del_class = DeletedClasses(class_id=group.id)
                db.session.add(del_class)
                db.session.commit()
            print("all")
    else:
        del_class = DeletedClasses(class_id=group.id)
        db.session.add(del_class)
        db.session.commit()
    return jsonify()


@app.route('/class_subjects/<int:class_id>', methods=["POST", "GET"])
def class_subjects(class_id):
    check_session()
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    classs = Class.query.filter(Class.id == class_id).first()
    subjects = Subject.query.all()
    return render_template('class_subjects/lesson.html', classs=classs, about_us=about_us, news=news, jobs=jobs,
                           about_id=about_id,
                           user=user, subjects=subjects)


@app.route('/add_class_subjects', methods=["POST", "GET"])
def add_class_subjects():
    info = request.get_json()["info"]
    print(info)
    classs = Class.query.filter(Class.id == int(info["class_id"])).first()
    print(classs)
    for subject in info["subjects"]:
        filter_subject = Subject.query.filter(Subject.id == int(subject)).first()
        print(filter_subject)
        classs.subjects.append(filter_subject)
        db.session.commit()
    if info["remove_subject"]:
        for subject in info["remove_subject"]:
            filter_subject = Subject.query.filter(Subject.id == int(subject)).first()
            classs.subjects.remove(filter_subject)
            db.session.commit()
    return jsonify()


@app.route('/flow', methods=["POST", "GET"])
def flow():
    add_lesson_time()
    discount_type()
    add_class_type()
    language_type()
    account_type()
    add_time_table_day()
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    print(user.id)
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    filter_info = []
    if about_us:
        about_id = about_us.id
    teachers = Teacher.query.all()
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    student_count = Student.query.count()
    students = Student.query.filter(Student.classes, Student.deleted_student == None).order_by(Student.id)
    pages = students.paginate(page=page, per_page=50)
    print(pages)
    # for page in pages.iter_count
    groups = Flow.query.all()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    languages = LanguageType.query.all()
    about_id = 0
    subjects = Subject.query.all()
    if about:
        about_id = about.id
    return render_template('flow/flow.html', about_us=about_us, about_id=about_id, pages=pages,
                           teachers=teachers, user=user, groups=groups, student_count=student_count, news=news,
                           jobs=jobs, languages=languages, subjects=subjects)


@app.route('/filter_student_for_flow', methods=["POST"])
def filter_student_for_flow():
    info = request.get_json()["info"]
    print(info)
    filter_student = []
    if info["search"] == "":
        if info['language_type'] == "all":
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes, Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = datetime.datetime.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            print(user)

                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name
                            }
                            filter_student.append(filtered)
            else:
                students = Student.query.filter(Student.class_number == info['class_number'],
                                                Student.classes, Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = datetime.datetime.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            print(user)
                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name
                            }
                            filter_student.append(filtered)
            print(filter_student)
        else:
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes,
                                                Student.language_type == info['language_type'],
                                                Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = datetime.datetime.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            print(user)

                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name
                            }
                            filter_student.append(filtered)
            else:
                students = Student.query.filter(Student.class_number == info['class_number'], Student.classes,
                                                Student.language_type == info['language_type'],
                                                Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = datetime.datetime.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            print(user)
                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name
                            }
                            filter_student.append(filtered)
            print(filter_student)
    else:
        if info['language_type'] == "all":
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes, Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = datetime.datetime.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            print(user)

                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name
                            }
                            filter_student.append(filtered)
            else:
                students = Student.query.filter(Student.class_number == info['class_number'],
                                                Student.classes, Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = datetime.datetime.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            print(user)
                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name
                            }
                            filter_student.append(filtered)
            print(filter_student)
        else:
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes,
                                                Student.language_type == info['language_type'],
                                                Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = datetime.datetime.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            print(user)

                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name
                            }
                            filter_student.append(filtered)
            else:
                students = Student.query.filter(Student.class_number == info['class_number'], Student.classes,
                                                Student.language_type == info['language_type'],
                                                Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = datetime.datetime.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            print(user)
                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name
                            }
                            filter_student.append(filtered)
            print(filter_student)
    return jsonify({
        "filter_student": filter_student
    })


@app.route('/search_not_student_for_flow', methods=["POST", "GET"])
def search_not_student_for_flow():
    search = request.get_json()["search"]
    users = User.query
    users = users.filter(or_(User.name.like('%' + search + '%'), User.surname.like('%' + search + '%')))
    users = users.order_by(User.name)
    filtered_users = []
    for user in users:
        if user.student:
            for filtered in user.student:
                if filtered.classes:
                    student = Student.query.filter(Student.user_id == user.id).first()
                    info = {
                        "id": user.id,
                        "name": user.name,
                        "surname": user.surname,
                        "age": user.age,
                        "number": user.number,
                        "language": student.language.name,
                        "image": user.image
                    }
                    filtered_users.append(info)
    return jsonify({
        "filtered_users": filtered_users
    })


@app.route('/creat_flow', methods=["POST", "GET"])
def creat_flow():
    class_info = request.get_json()['flow_info']
    class_name = class_info['name']
    subject_id = class_info["subject_id"]
    teacher_id = class_info['teacher_id']
    add_flow = Flow(name=class_name, subject_id=subject_id, teacher_id=teacher_id)
    db.session.add(add_flow)
    db.session.commit()
    students = class_info['students']
    for student in students:
        print(student)
        filter_student = Student.query.filter(Student.user_id == int(student)).first()
        add_flow.students.append(filter_student)
        db.session.commit()
    print(class_name)
    return jsonify()


@app.route('/join_flow', methods=["POST", "GET"])
def join_flow():
    join_class = request.get_json()["join_class"]
    group = Flow.query.filter(Flow.id == join_class['class_id']).first()
    for st in join_class['students']:
        student = Student.query.filter(Student.user_id == int(st)).first()
        group.students.append(student)
        db.session.commit()
    return jsonify()
