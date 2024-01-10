from app import *
from backend.models.basic_model import *
from backend.settings.settings import *


@app.route('/vacation', methods=['POST', 'GET'])
def vacation():
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    jobs_list = Info.query.filter(Info.type_id == 3).order_by(Info.id).all()
    vacations = Vacation.query.order_by(Vacation.id).all()
    if request.method == "POST":
        text = request.form.get('text')
        job_id = request.form.get('job_id')
        add = Vacation(info_id=job_id, text=text)
        add.add()
        return redirect(url_for('vacation'))
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    return render_template('vacation/index.html', jobs=jobs, vacations=vacations, jobs_list=jobs_list,
                           about_id=about_id, about_us=about_us, user=user,
                           news=news)


@app.route('/edit_vacation/<int:vacation_id>', methods=['POST'])
def edit_vacation(vacation_id):
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    text = request.form.get('text')
    job_id = request.form.get('job_id')
    Vacation.query.filter(Vacation.id == vacation_id).update({
        "info_id": job_id,
        "text": text
    })
    db.session.commit()
    return redirect(url_for('vacation'))


@app.route('/delete_vacation/<int:vacation_id>')
def delete_vacation(vacation_id):
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    Vacation.query.filter(Vacation.id == vacation_id).delete()
    db.session.commit()
    return redirect(url_for('vacation'))


@app.route('/work_info', methods=['POST', 'GET'])
def work_info():
    jobs = Info.query.filter(Info.type_id == 3).order_by(Info.id).all()
    vacations = Vacation.query.order_by(Vacation.id).all()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    if about_us:
        about_id = about_us.id
    return render_template('front/vacation/vakansiyalar.html', jobs=jobs, vacations=vacations, about_id=about_id)


@app.route('/application_workers', methods=['POST', 'GET'])
def application_workers():
    if request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        number = request.form.get("number")
        photo = request.files['img']

    return redirect(url_for("work_info"))


@app.route('/send_request/<int:vacation_id>', methods=['POST'])
def send_request(vacation_id):
    name = request.form.get('name')
    surname = request.form.get('surname')
    phone = request.form.get('phone')
    file = request.files.get('file')

    if file:
        photo_file = secure_filename(file.filename)
        photo_url = "static/other_files" + "/" + photo_file
        app.config['UPLOAD_FOLDER'] = "static/other_files"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
        add = Requests(name=name, surname=surname, phone=phone, vacation_id=vacation_id, add_date=datetime.now(),
                       pdf_file=photo_url)
        add.add()
    else:
        add = Requests(name=name, surname=surname, phone=phone, vacation_id=vacation_id, add_date=datetime.now(),)
        add.add()
    return redirect(url_for('work_info'))


@app.route('/get_request/<int:vacation_id>')
def get_request(vacation_id):
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    requests = Requests.query.filter(Requests.vacation_id == vacation_id).order_by(Requests.id).all()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    return render_template('requests/Index.html', requests=requests, about_us=about_us, news=news, about_id=about_id,
                           jobs=jobs, user=user)


@app.route('/get_pdf/<int:request_id>')
def get_pdf(request_id):
    check_session()
    request = Requests.query.filter(Requests.id == request_id).first()
    return send_file(f"{request.pdf_file}", as_attachment=True)


@app.route('/delete_request/<int:request_id>')
def delete_request(request_id):
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    request = Requests.query.filter(Requests.id == request_id).first()
    vacation_id = request.vacation_id
    Requests.query.filter(Requests.id == request_id).delete()
    db.session.commit()
    return redirect(url_for('get_request', vacation_id=vacation_id))


@app.route('/comments')
def comments():
    check_session()
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    comments = Comments.query.order_by(Comments.id).all()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    return render_template('comment/murojat.html', comments=comments, about_us=about_us, about_id=about_id, news=news,
                           jobs=jobs, user=user)


@app.route('/delete_comment/<int:comment_id>')
def delete_comment(comment_id):
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    Comments.query.filter(Comments.id == comment_id).delete()
    db.session.commit()
    return redirect(url_for('comments'))
