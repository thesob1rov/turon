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
