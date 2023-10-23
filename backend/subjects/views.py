from app import *
from backend.models.basic_model import Subject


@app.route('/add_subject', methods=["POST", "GET"])
def add_subject():

    """
    subject qoishish
    :return:
    """
    error = check_session()
    if error:
        return redirect(url_for('home'))
    if request.method == "POST":
        subject = request.form.get("name")
        add = Subject(name=subject)
        db.session.add(add)
        db.session.commit()
    return redirect(url_for("subject_list"))


@app.route('/subject_list', methods=["POST", "GET"])
def subject_list():
    """
    subjectlani listi
    :return:
    """
    user = current_user()
    error = check_session()
    if error:
        return redirect(url_for('home'))
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    subjects = Subject.query.all()
    return render_template('subjects_list/book_list.html', about_us=about_us, news=news, jobs=jobs, about_id=about_id,
                           user=user, subjects=subjects)


@app.route('/change_subjects', methods=["POST", "GET"])
def change_subjects():
    """
    subjectni ozgartirish
    :return:
    """
    info = request.get_json()["info"]
    Subject.query.filter(Subject.id == info["subject_id"]).update({
        "name": info["subject_name"]
    })
    db.session.commit()
    return jsonify()


@app.route('/delete_subjects', methods=["POST", "GET"])
def delete_subjects():
    """
    subject ochirish
    :return:
    """
    info = request.get_json()["info"]
    Subject.query.filter(Subject.id == int(info)).delete()
    db.session.commit()
    return jsonify()
