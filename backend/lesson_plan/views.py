from app import *
from datetime import datetime
from backend.settings.settings import *


@app.route('/lesson_plan/<int:teacher_id>', methods=['POST', 'GET'])
def lesson_plan(teacher_id):
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = User.query.filter(User.id == teacher_id).first()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    if about_us:
        about_id = about_us.id
    return render_template('lesson_plan/index.html', user=user, about_us=about_us, news=news, jobs=jobs,
                           about=about, about_id=about_id)
