from app import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.settings.settings import *
# from datetime import datetime
from werkzeug.utils import secure_filename
import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def users_folder():
    upload_folder = "static/user_image/"
    return upload_folder


def checkFile(filename):
    value = '.' in filename
    type_file = filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return value and type_file


def user_password_update():
    users = User.query.filter(User.id >= 70, User.id <= 140).all()
    print(len(users))
    for user in users:
        password = "12345678"
        hashed = generate_password_hash(password=password)
        User.query.filter(User.id == user.id).update({
            "password": hashed
        })
        db.session.commit()


@app.route('/')
def home():
    add_targetolog()
    user = current_user()
    # user_password_update()
    create_menu()
    news = Info.query.filter(Info.type_id == 2).order_by(desc(Info.id)).limit(3)
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    if about_us:
        about_id = about_us.id
    return render_template('home/index.html', news=news, about_id=about_id, about_us=about_us, user=user)




def add_targetolog():
    username = "targetolog"
    name = "targetolog"
    surname = "targetolog"
    password = "12345678"
    role = "targetolog"
    hashed = generate_password_hash(password=password)
    user_target = User.query.filter(User.username == username).first()
    if not user_target:
        add = User(username=username, name=name, surname=surname, password=hashed, role=role)
        db.session.add(add)
        db.session.commit()



@app.route('/education')
def education():
    user = current_user()

    news = Info.query.filter(Info.type_id == 2).order_by(desc(Info.id)).limit(3)
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    if about_us:
        about_id = about_us.id
    return render_template('front/education/lesson.html', user=user, about_id=about_id, about_us=about_us, news=news)


@app.route('/time_table')
def time_table():
    user = current_user()
    news = Info.query.filter(Info.type_id == 2).order_by(desc(Info.id)).limit(3)
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    if about_us:
        about_id = about_us.id
    return render_template('front/time_table/calendars.html', user=user, about_id=about_id, about_us=about_us,
                           news=news)


@app.route('/register', methods=['POST', 'GET'])
def register():
    class_types = ClassType.query.order_by(ClassType.id).all()
    languages = LanguageType.query.all()
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        surname = request.form.get("surname")
        parent_name = request.form.get("parent_name")
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")
        password = request.form.get("password")
        number = request.form.get("number")
        class_number = request.form.get("class_number")
        language = request.form.get("language")
        hashed = generate_password_hash(password=password)
        datetime_str = f'{year}-{month}-{day}'
        datetime_object = datetime.datetime.strptime(datetime_str, '%Y-%m-%d')
        birth_year = year
        current_year = datetime.datetime.now()
        age = int(current_year.year) - int(birth_year)
        add = User(name=name, username=username, surname=surname, parent_name=parent_name, birth_date=datetime_object,
                   password=hashed, number=number, age=age)
        add.add()
        student = Student(user_id=add.id, class_number=class_number, language_type=language)
        student.add()
        filter_student = Student.query.filter(Student.user_id == student.user_id).first()
        today = datetime.datetime.today()
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
            add = StudentMonthPayments(student_id=filter_student.id, month=data_object,
                                       class_price=filter_student.class_type.price,
                                       payed=0, another=filter_student.class_type.price,
                                       real_price=filter_student.class_type.price)
            db.session.add(add)
            db.session.commit()
        return redirect(url_for('register'))
    return render_template('register/register.html', languages=languages, class_types=class_types)


@app.route('/login', methods=['POST', 'GET'])
def login():
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    if about_us:
        about_id = about_us.id
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        username_sign = User.query.filter_by(username=username).first()

        if username_sign and check_password_hash(username_sign.password, password):
            session['username'] = username
            if username_sign.role == "targetolog":
                return redirect(url_for('admin'))
            if username_sign.role == "admin":
                return redirect(url_for('student'))
    return render_template('login/login.html')


@app.route('/logout')
def logout():
    session['username'] = None
    return redirect(url_for('home'))


@app.route('/admin')
def admin():
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
    return render_template('admin/index.html', about_us=about_us, news=news, jobs=jobs, about_id=about_id, user=user)


@app.route('/add_comment', methods=['POST'])
def add_comment():
    text = request.form.get('text')
    add = Comments(text=text, add_date=datetime.now())
    db.session.add(add)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/profile/<int:user_id>', methods=['POST', 'GET'])
def profile(user_id):
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = User.query.filter(User.id == user_id).first()
    if user.birth_date:
        birth_year = user.birth_date
        current_year = datetime.datetime.now()
        age = int(current_year.year) - int(birth_year.year)
        User.query.filter(User.id == user_id).update({
            "age": age
        })
        db.session.commit()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    if about_us:
        about_id = about_us.id
    return render_template('profile/profile.html', user=user, about_us=about_us, news=news, jobs=jobs,
                           about=about, about_id=about_id)


@app.route('/edit_profile/<int:user_id>', methods=['POST', 'GET'])
def edit_profile(user_id):
    class_types = ClassType.query.order_by(ClassType.id).all()
    user = User.query.filter(User.id == user_id).first()
    student = Student.query.filter(Student.user_id == user.id).first()
    error = check_session()
    if error:
        return redirect(url_for('home'))
    languages = LanguageType.query.all()
    curr_user = current_user()
    if request.method == "POST":
        if curr_user.role == 'admin' or curr_user.role == 'director':
            username = request.form.get("username")
            if not student.class_type:
                class_type = request.form.get("class_type")
                Student.query.filter(Student.user_id == user.id).update({
                    "class_number": class_type
                })
                db.session.commit()
                today = datetime.datetime.today()
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
                    add = StudentMonthPayments(student_id=student.id, month=data_object,
                                               class_price=student.class_type.price,
                                               payed=0, another=student.class_type.price,
                                               real_price=student.class_type.price)
                    db.session.add(add)
                    db.session.commit()
            name = request.form.get("name")
            surname = request.form.get("surname")
            parent_name = request.form.get("parent_name")
            address = request.form.get("address")
            email = request.form.get("email")
            day = request.form.get("day")
            month = request.form.get("month")
            year = request.form.get("year")
            number = request.form.get("number")
            language_type = request.form.get("language_type")
            photo = request.files["photo"]
            datetime_str = f'{year}-{month}-{day}'
            datetime_object = datetime.datetime.strptime(datetime_str, '%Y-%m-%d')
            folder = users_folder()
            if photo and checkFile(photo.filename):
                photo_file = secure_filename(photo.filename)
                photo_url = '/' + folder + photo_file
                app.config['UPLOAD_FOLDER'] = folder
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
                User.query.filter(User.id == user_id).update({
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
                User.query.filter(User.id == user_id).update({
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
            filter_language = LanguageType.query.filter(LanguageType.id == language_type).first()
            Student.query.filter(Student.user_id == user_id).update({
                "language_type": filter_language.id
            })
            db.session.commit()
            return redirect(url_for("student_profile", student_id=user.id))
        else:
            username = request.form.get("username")
            photo = request.files["photo"]
            folder = users_folder()
            if photo and checkFile(photo.filename):
                photo_file = secure_filename(photo.filename)
                photo_url = '/' + folder + photo_file
                app.config['UPLOAD_FOLDER'] = folder
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
                User.query.filter(User.id == user_id).update({
                    "username": username,
                    "image": photo_url
                })
                db.session.commit()
            else:
                User.query.filter(User.id == user_id).update({
                    "username": username
                })
                db.session.commit()
            return redirect(url_for("student_profile", student_id=user.id))
    return render_template('edit_profile/edit.html', user=user, curr_user=curr_user, languages=languages,
                           class_types=class_types)
