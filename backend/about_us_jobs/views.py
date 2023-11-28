from app import *
from backend.models.basic_model import *
from backend.settings.settings import *
from backend.student.routes import *

@app.route('/about_front/<int:type_id>/<int:info_id>')
def about_front(type_id, info_id):
    error = check_session()
    if error:
        return redirect(url_for('home'))
    if info_id == 0:
        info_id = None
    infos = Info.query.filter(Info.type_id == type_id).order_by(Info.id).all()
    current_info = Info.query.filter(Info.id == info_id).order_by(Info.id).first()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    if about_us:
        about_id = about_us.id
    return render_template('front/about_us/index.html', current_info=current_info, infos=infos, about_id=about_id)


@app.route('/get_about_profile/<int:type_id>/<int:info_id>', methods=['POST', 'GET'])
def get_about_profile(type_id, info_id):
    discount_type()
    add_class_type()
    error = check_session()
    if error:
        return redirect(url_for('home'))
    language_type()
    account_type()
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    if info_id == 0:
        info_id = None
    infos = Info.query.filter(Info.type_id == type_id).order_by(Info.id).all()
    current_info = Info.query.filter(Info.id == info_id).order_by(Info.id).first()
    if request.method == "POST":
        title = request.form.get('title')
        text = request.form.get('text')
        img = request.files['img']
        if img:
            filename = secure_filename(img.filename)
            img_url = "/static/img/about_us_jobs/" + filename
            app.config['UPLOADED_FOLDER'] = "static/img/about_us_jobs"

            img.save(os.path.join(app.config['UPLOADED_FOLDER'], img.filename))
            add_info = Info(title=title, text=text, img=img_url, type_id=type_id)
            add_info.add()
        else:
            add_info = Info(title=title, text=text, type_id=type_id)
            add_info.add()
        return redirect(url_for('get_about_profile', type_id=type_id, info_id=add_info.id))
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    return render_template('about_us/index.html', type_id=type_id, infos=infos, current_info=current_info, news=news,
                           about_us=about_us, about_id=about_id, jobs=jobs, user=user)


@app.route('/infos/<int:type_id>', methods=['POST', 'GET'])
def infos(type_id):
    check_session()
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    jobs_list = Info.query.filter(Info.type_id == type_id).order_by(Info.id).all()
    if request.method == "POST":
        title = request.form.get('title')
        text = request.form.get('text')
        img = request.files['img']

        if img:
            filename = secure_filename(img.filename)
            img_url = "/static/img/about_us_jobs/" + filename
            app.config['UPLOADED_FOLDER'] = "static/img/about_us_jobs"

            img.save(os.path.join(app.config['UPLOADED_FOLDER'], img.filename))
            add_info = Info(title=title, text=text, img=img_url, type_id=type_id)
            add_worker = Job(name=title)
            add_worker.add()
            add_info.add()
        else:
            add_info = Info(title=title, text=text, type_id=type_id)
            add_info.add()
            add_worker = Job(name=title)
            add_worker.add()
        return redirect(url_for('infos', type_id=type_id))
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    return render_template('jobs/index.html', jobs_list=jobs_list, type_id=type_id, news=news, jobs=jobs,
                           about_id=about_id, about_us=about_us, user=user)


@app.route('/edit_info/<int:info_id>', methods=['POST'])
def edit_info(info_id):
    check_session()
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    title = request.form.get('title')
    text = request.form.get('text')
    img = request.files['img']

    info = Info.query.filter(Info.id == info_id).first()
    if img:

        types = Info.query.filter(Info.img == info.img, Info.id != info.id).first()
        if not types and info.img:
            if os.path.isfile(info.img[1:]):
                os.remove(info.img[1:])
        filename = secure_filename(img.filename)
        img_url = "/static/img/about_us_jobs/" + filename
        app.config['UPLOADED_FOLDER'] = "static/img/about_us_jobs"

        img.save(os.path.join(app.config['UPLOADED_FOLDER'], img.filename))
        Info.query.filter(Info.id == info_id).update({
            "title": title,
            "text": text,
            "img": img_url
        })
    Info.query.filter(Info.id == info_id).update({
        "title": title,
        "text": text,
    })
    db.session.commit()
    if info.type_id == 1:
        return redirect(url_for('get_about_profile', type_id=info.type_id, info_id=info_id))
    elif info.type_id == 3:
        return redirect(url_for('infos', type_id=info.type_id))


@app.route('/delete_info/<int:info_id>')
def delete_info(info_id):
    check_session()
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    info = Info.query.filter(Info.id == info_id).first()
    type_id = info.type_id
    Info.query.filter(Info.id == info_id).delete()
    db.session.commit()
    get_info = Info.query.order_by(Info.id).first()
    if type_id == 1:
        if get_info:
            return redirect(url_for('get_about_profile', type_id=type_id, info_id=get_info.id))
        else:
            return redirect(url_for('get_about_profile', type_id=type_id, info_id=0))
    elif type_id == 3:
        return redirect(url_for('infos', type_id=type_id))
