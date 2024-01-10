from app import *
from backend.settings.settings import *

from datetime import datetime as dt
import datetime


def pdf_folder():
    upload_folder = "static/pdf_contract/"
    return upload_folder


def add_lesson_time():
    lessons = [
        {
            "lesson_count": "1",
            "start": "8:30",
            "end": "9:15"
        },
        {
            "lesson_count": "breakfast",
            "start": "9:15",
            "end": "9:45"
        },
        {
            "lesson_count": "2",
            "start": "9:45",
            "end": "10:30"
        },
        {
            "lesson_count": "3",
            "start": "10:35",
            "end": "11:20"
        },
        {
            "lesson_count": "4",
            "start": "11:25",
            "end": "12:10"
        },
        {
            "lesson_count": "5",
            "start": "12:15",
            "end": "13:00"
        },
        {
            "lesson_count": "5",
            "start": "13:10",
            "end": "13:55"
        },
        {
            "lesson_count": "6",
            "start": "14:00",
            "end": "14:45"
        },
        {
            "lesson_count": "7",
            "start": "14:50",
            "end": "15:35"
        }
    ]

    for lesson in lessons:
        filter_time_list = TimeList.query.filter(TimeList.lesson_count == lesson["lesson_count"],
                                                 TimeList.start == lesson["start"],
                                                 TimeList.end == lesson["end"]).first()
        if not filter_time_list:
            add = TimeList(lesson_count=lesson["lesson_count"], start=lesson["start"], end=lesson["end"])
            db.session.add(add)
            db.session.commit()


def add_class_type():
    class_types = [
        {
            "class_number": 0,
            "price": 2500000
        },
        {
            "class_number": 1,
            "price": 3500000
        },
        {
            "class_number": 2,
            "price": 3500000
        },
        {
            "class_number": 3,
            "price": 3500000
        },
        {
            "class_number": 4,
            "price": 3500000
        },
        {
            "class_number": 5,
            "price": 3700000
        },
        {
            "class_number": 6,
            "price": 3700000
        },
        {
            "class_number": 7,
            "price": 3700000
        },
        {
            "class_number": 8,
            "price": 4500000
        },
        {
            "class_number": 9,
            "price": 4500000
        },
        {
            "class_number": 10,
            "price": 4800000
        },
        {
            "class_number": 11,
            "price": 4800000
        }
    ]
    for class_type in class_types:
        filter_class = ClassType.query.filter(ClassType.class_number == class_type["class_number"]).first()
        if not filter_class:
            add = ClassType(class_number=class_type["class_number"], price=class_type["price"])
            db.session.add(add)
            db.session.commit()


def language_type():
    languages = [
        "UZ",
        "RUS"
    ]

    for language in languages:
        filter = LanguageType.query.filter(LanguageType.name == language).first()

        if not filter:
            add = LanguageType(name=language)
            db.session.add(add)
            db.session.commit()


def account_type():
    account_types = [
        "bank",
        "click",
        "cash"
    ]

    for account_type in account_types:
        filter = AccountType.query.filter(AccountType.name == account_type).first()

        if not filter:
            add = AccountType(name=account_type)
            db.session.add(add)
            db.session.commit()


def discount_type():
    discount_types = [
        "2 ta va undan ortiq farzand",
        "yillik to'lov"
    ]
    for discount_type in discount_types:
        filter = DiscountType.query.filter(DiscountType.name == discount_type).first()
        if not filter:
            add = DiscountType(name=discount_type)
            db.session.add(add)
            db.session.commit()


def add_time_table_day():
    days = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday"
    ]
    for day in days:
        filter_day = TimeTableDay.query.filter(TimeTableDay.name == day).first()
        if not filter_day:
            add = TimeTableDay(name=day)
            db.session.add(add)
            db.session.commit()


def add_class_type_for_old_students():
    students = Student.query.filter(Student.student_month_payments == None, Student.classes).all()
    for student in students:
        print(student.classes)
        # if student.classes:
        for classs in student.classes:
            print(classs.class_number)
            class_type = ClassType.query.filter(ClassType.class_number == classs.class_number).first()
            Student.query.filter(Student.id == student.id).update({
                "class_number": class_type.id
            })
            db.session.commit()
        filter_student = Student.query.filter(Student.user_id == student.user_id).first()
        today = dt.today()
        print(filter_student.class_type)

        month_list = []
        if today.month == 1:
            start = datetime.date(today.year, 9, today.day)
            end = datetime.date(today.year, 5, 1)
            for delta in range((end - start).days + 1):
                result_date = start + datetime.timedelta(days=delta)
                months = f'{result_date.month}-1-{result_date.year}'
                if not months in month_list:
                    month_list.append(months)
        else:
            start = datetime.date(today.year, 9, today.day)
            next_year = today.year + 1
            end = datetime.date(next_year, 5, 1)
            for delta in range((end - start).days + 1):
                result_date = start + datetime.timedelta(days=delta)
                months = f'{result_date.month}-1-{result_date.year}'
                if not months in month_list:
                    month_list.append(months)
        for month in month_list:
            data_object = datetime.datetime.strptime(month, '%m-%d-%Y')
            add = StudentMonthPayments(student_id=filter_student.id, month=data_object,
                                       class_price=filter_student.class_type.price,
                                       payed=0, another=filter_student.class_type.price,
                                       real_price=filter_student.class_type.price)
            db.session.add(add)
            db.session.commit()


@app.route('/student', methods=["POST", "GET"])
def student():
    """
    studentlani spiska page
    :return:
    """
    add_class_type_for_old_students()
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
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    filter_info = []
    if about_us:
        about_id = about_us.id
    teachers = Teacher.query.filter(Teacher.deleted_teacher == None).all()
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    student_count = Student.query.count()
    students = Student.query.filter(Student.classes == None, Student.deleted_student == None).order_by(Student.id)
    pages = students.paginate(page=page, per_page=50)
    # for page in pages.iter_count
    groups = Class.query.filter(Class.deleted_classes == None).all()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    languages = LanguageType.query.all()
    about_id = 0
    if about:
        about_id = about.id
    clients_count = Clients.query.count()
    return render_template('student/index.html', about_us=about_us, about_id=about_id, pages=pages,
                           teachers=teachers, user=user, groups=groups, student_count=student_count, news=news,
                           jobs=jobs, languages=languages, clients_count=clients_count)


@app.route('/clients', methods=["POST", "GET"])
def clients():
    user = current_user()
    error = check_session()
    if error:
        return redirect(url_for('home'))
    groups = Class.query.filter(Class.deleted_classes == None).all()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    clients = Clients.query.all()
    return render_template("clients/cliants.html", about_us=about_us, about_id=about_id,
                           user=user, groups=groups, news=news,
                           jobs=jobs, clients=clients)


@app.route('/delete_clients/<int:client_id>', methods=["POST", "GET"])
def delete_clients(client_id):
    Clients.query.filter(Clients.id == client_id).delete()
    db.session.commit()
    return redirect(url_for("clients"))


@app.route('/filter_student', methods=["POST"])
def filter_student():
    """
    yangi studentlani filteri
    :return: filterlangan studentlani yuvoradi
    """
    info = request.get_json()["info"]

    filter_student = []
    if info["search"] == "":
        if info['language_type'] == "all":
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes == None, Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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
                                                Student.classes == None, Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes == None,
                                                Student.language_type == info['language_type'],
                                                Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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
                students = Student.query.filter(Student.class_number == info['class_number'], Student.classes == None,
                                                Student.language_type == info['language_type'],
                                                Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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
        if info['language_type'] == "all":
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes == None, Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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
                                                Student.classes == None, Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes == None,
                                                Student.language_type == info['language_type'],
                                                Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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
                students = Student.query.filter(Student.class_number == info['class_number'], Student.classes == None,
                                                Student.language_type == info['language_type'],
                                                Student.deleted_student == None).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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

    return jsonify({
        "filter_student": filter_student
    })


@app.route('/filter_student_old', methods=["POST"])
def filter_student_old():
    """
    sinifi bor stduentlani filteri
    :return: filterlangan sinifi bor studentlani listini yuvoradi
    """
    info = request.get_json()["info"]
    filter_student = []
    if info["search"] == "":
        if info['language_type'] == "all":
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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
                students = Student.query.filter(Student.class_number == info['class_number'], Student.classes).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes,
                                                Student.language_type == info['language_type']).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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
                                                Student.language_type == info['language_type']).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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
        if info['language_type'] == "all":
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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
                students = Student.query.filter(Student.class_number == info['class_number'], Student.classes).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes,
                                                Student.language_type == info['language_type']).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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
                                                Student.language_type == info['language_type']).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
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

    return jsonify({
        "filter_student": filter_student
    })


@app.route('/get_students', methods=["GET"])
def get_students():
    """
    xamma studentlani js ga yuvorish uchun funksiya
    :return: stduentlani yuvoradi
    """
    student_list = []
    students = Student.query.all()

    for student in students:
        users = User.query.filter(User.id == student.user_id).all()
        birth_year = student.user.birth_date
        current_year = dt.now()
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
            student_list.append(filtered)
    return jsonify({
        "student_list": student_list
    })


@app.route('/student_profile/<int:student_id>', methods=["POST", "GET"])
def student_profile(student_id):
    """
    student profili
    :param student_id:
    :return:
    """
    error = check_session()
    if error:
        return redirect(url_for('home'))
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    languages = LanguageType.query.all()
    about_id = 0
    if about:
        about_id = about.id
    user = current_user()
    student = Student.query.filter(Student.user_id == student_id).first()
    students = None
    for cl in student.classes:
        group = Class.query.filter(Class.id == cl.id).first()

        students = len(group.student)
    return render_template('user_profile/index.html', student=student, students=students, user=user, about_us=about_us,
                           news=news, jobs=jobs, about_id=about_id, languages=languages
                           )


@app.route('/not_in_class_student')
def not_in_class_student():
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    students = Student.query.all()
    student_list = []
    for student in students:
        if not student.classes:
            student_list.append(student)
    if about_us:
        about_id = about_us.id
    teachers = Teacher.query.all()
    return render_template('not class student/index.html', user=user, student_list=student_list, teachers=teachers,
                           about_us=about_us, about_id=about_id)


@app.route('/join_class', methods=["POST", "GET"])
def join_class():
    """
    bor siniflarga student qoshish
    :return:
    """
    join_class = request.get_json()["join_class"]
    group = Class.query.filter(Class.id == join_class['class_id']).first()
    for st in join_class['students']:
        student = Student.query.filter(Student.user_id == int(st)).first()
        student.classes.append(group)
        db.session.commit()
        today = datetime.today()
        month_list = []
        if today.month == 1:
            start = datetime.date(today.year, today.month, today.day)
            end = datetime.date(today.year, 5, 1)

            for delta in range((end - start).days + 1):
                result_date = start + datetime.timedelta(days=delta)
                months = f'{result_date.month}-1-{result_date.year}'
                if not months in month_list:
                    month_list.append(months)

        else:
            start = datetime.date(today.year, today.month, today.day)
            next_year = today.year + 1
            end = datetime.date(next_year, 5, 1)
            for delta in range((end - start).days + 1):
                result_date = start + datetime.timedelta(days=delta)
                months = f'{result_date.month}-1-{result_date.year}'
                if not months in month_list:
                    month_list.append(months)
        for month in month_list:
            data_object = datetime.datetime.strptime(month, '%m-%d-%Y')
            add = StudentMonthPayments(student_id=student.id, month=data_object)
            db.session.add(add)
            db.session.commit()
    return jsonify()


@app.route('/edit_user_password', methods=["POST", "GET"])
def edit_user_password():
    """
    user parolini ozgartiradi
    :return:
    """
    user = current_user()
    info = request.get_json()["info"]
    hashed = generate_password_hash(password=info, method="sha256")
    User.query.filter(User.id == user.id).update({
        "password": hashed
    })
    db.session.commit()
    return jsonify()


@app.route('/edit_username', methods=["POST", "GET"])
def edit_username():
    """
    userusernameni ozgartiradi
    :return:
    """
    user = current_user()
    info = request.get_json()["info"]
    User.query.filter(User.id == user.id).update({
        "username": info
    })
    db.session.commit()
    return jsonify()


@app.route('/old_student', methods=["POST", "GET"])
def old_student():
    """
    sinifi bor studentlani pagesi
    :return:
    """
    user = current_user()
    error = check_session()
    if error:
        return redirect(url_for('home'))
    languages = LanguageType.query.all()

    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    if about_us:
        about_id = about_us.id
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    student_count = Student.query.count()
    students = Student.query.filter(Student.classes)
    pages = students.paginate(page=page, per_page=50)
    groups = Class.query.all()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    return render_template('old_student/old_student.html', about_us=about_us, about_id=about_id, pages=pages,
                           user=user, groups=groups, student_count=student_count, news=news,
                           jobs=jobs, languages=languages)


@app.route('/pdf_contract/<int:student_id>', methods=["POST", "GET"])
def pdf_contract(student_id):
    """
    studentni pdf shartnomasi
    :param student_id:
    :return:
    """
    error = check_session()
    if error:
        return redirect(url_for('home'))

    user = current_user()
    student = User.query.filter(User.id == student_id).first()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    if request.method == "POST":
        pdf = request.files['pdf']
        folder = pdf_folder()
        if pdf and checkFile(pdf.filename):
            photo_file = secure_filename(pdf.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            add = PdfContract(user_id=student.id, pdf=photo_url)
            db.session.add(add)
            db.session.commit()
            return redirect(url_for("create_contract", student_id=student.id))
    return render_template('contract/contract.html', about_us=about_us, news=news, jobs=jobs, about_id=about_id,
                           user=user, student=student)


@app.route('/search_not_student_in_class', methods=["POST", "GET"])
def search_not_student_in_class():
    """
    sinifi yo'q studentlani filterlash
    :return:
    """
    search = request.get_json()["search"]
    users = User.query
    users = users.filter(or_(User.name.like('%' + search + '%'), User.surname.like('%' + search + '%')))
    users = users.order_by(User.name)
    filtered_users = []
    for user in users:
        if user.student:
            for filtered in user.student:
                if not filtered.classes:
                    student = Student.query.filter(Student.user_id == user.id, Student.deleted_student == None).first()
                    info = {
                        "id": user.id,
                        "name": user.name,
                        "surname": user.surname,
                        "age": user.age,
                        "number": user.number,
                        "image": user.image
                    }
                    if student.language:
                        info["language"] = student.language.name
                    else:
                        info["language"] = "kiritilmagan"
                    filtered_users.append(info)
    return jsonify({
        "filtered_users": filtered_users
    })


@app.route('/search_student_in_class', methods=["POST", "GET"])
def search_student_in_class():
    """
    sinifi bor studentlani filterlash
    :return:
    """
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
                        # "language": student.language.name,
                        "image": user.image
                    }
                    if student.language:
                        info["language"] = student.language.name
                    else:
                        info["language"] = "kiritilmagan"
                    filtered_users.append(info)
    return jsonify({
        "filtered_users": filtered_users
    })


@app.route('/delete_student', methods=["POST", "GET"])
def delete_student():
    """
    studentni ochirish
    :return:
    """
    id = request.get_json()["id"]
    add = DeletedStudent(student_id=id)
    db.session.add(add)
    db.session.commit()
    return jsonify()


@app.route('/deleted_students', methods=["POST", "GET"])
def deleted_students():
    """
    ochirilgan studentlar
    :return:
    """
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    student_count = Student.query.filter(Student.deleted_student).count()
    students = Student.query.filter(Student.classes == None, Student.deleted_student).order_by(Student.id)
    pages = students.paginate(page=page, per_page=50)

    languages = LanguageType.query.all()
    return render_template('deleted_student_list/deleted_student_list.html', about_us=about_us, news=news, jobs=jobs,
                           about_id=about_id,
                           user=user, student=student, student_count=student_count, pages=pages, languages=languages)


@app.route('/return_students', methods=["POST", "GET"])
def return_students():
    """
    ochirilgan studentlani qaytarish
    :return:
    """
    id = request.get_json()["id"]
    DeletedStudent.query.filter(DeletedStudent.student_id == id).delete()
    db.session.commit()
    return jsonify()


@app.route('/filter_delete_student', methods=["POST", "GET"])
def filter_delete_student():
    """
    ochirilgan syudentlani filteri
    :return:
    """
    info = request.get_json()["info"]

    filter_student = []
    if info["search"] == "":
        if info['language_type'] == "all":
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes == None, Student.deleted_student).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = datetime.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name,
                                "student": student.id
                            }
                            filter_student.append(filtered)
            else:
                students = Student.query.filter(Student.class_number == info['class_number'],
                                                Student.classes == None, Student.deleted_student).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name,
                                "student": student.id
                            }
                            filter_student.append(filtered)

        else:
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes == None,
                                                Student.language_type == info['language_type'],
                                                Student.deleted_student).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name,
                                "student": student.id
                            }
                            filter_student.append(filtered)
            else:
                students = Student.query.filter(Student.class_number == info['class_number'], Student.classes == None,
                                                Student.language_type == info['language_type'],
                                                Student.deleted_student).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name,
                                "student": student.id
                            }
                            filter_student.append(filtered)

    else:
        if info['language_type'] == "all":
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes == None, Student.deleted_student).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name,
                                "student": student.id
                            }
                            filter_student.append(filtered)
            else:
                students = Student.query.filter(Student.class_number == info['class_number'],
                                                Student.classes == None, Student.deleted_student).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name,
                                "student": student.id
                            }
                            filter_student.append(filtered)

        else:
            if info['class_number'] == 'sinflar':
                students = Student.query.filter(Student.classes == None,
                                                Student.language_type == info['language_type'],
                                                Student.deleted_student).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name,
                                "student": student.id
                            }
                            filter_student.append(filtered)
            else:
                students = Student.query.filter(Student.class_number == info['class_number'], Student.classes == None,
                                                Student.language_type == info['language_type'],
                                                Student.deleted_student).all()
                for student in students:
                    users = User.query.filter(User.id == student.user_id,
                                              or_(User.name.like('%' + info['search'] + '%'),
                                                  User.surname.like('%' + info['search'] + '%'))).all()
                    birth_year = student.user.birth_date
                    current_year = dt.now()
                    age = int(current_year.year) - int(birth_year.year)
                    for user in users:
                        if age >= int(info['from']) and age <= int(info['to']):
                            filtered = {
                                "id": user.id,
                                "username": user.username,
                                "name": user.name,
                                "birth_date": user.birth_date,
                                "number": user.number,
                                "image": user.image,
                                "surname": user.surname,
                                "age": age,
                                "language": student.language.name,
                                "student": student.id
                            }
                            filter_student.append(filtered)

    return jsonify({
        "filter_student": filter_student
    })


@app.route('/search_delete_student', methods=["POST", "GET"])
def search_delete_student():
    """
    ochirilgan studentlani qidirish
    :return:
    """
    search = request.get_json()["search"]
    users = User.query
    users = users.filter(or_(User.name.like('%' + search + '%'), User.surname.like('%' + search + '%')))
    users = users.order_by(User.name)
    filtered_users = []
    for user in users:
        if user.student:
            for filtered in user.student:
                if filtered.deleted_student:
                    student = Student.query.filter(Student.user_id == user.id, Student.deleted_student).first()
                    info = {
                        "id": user.id,
                        "name": user.name,
                        "surname": user.surname,
                        "age": user.age,
                        "number": user.number,
                        "image": user.image,
                        "student": student.id
                    }
                    if student.language:
                        info["language"] = student.language.name
                    else:
                        info["language"] = "kiritilmagan"
                    filtered_users.append(info)
    return jsonify({
        "filtered_users": filtered_users
    })
