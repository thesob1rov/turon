from app import *
from backend.models.basic_model import *


@app.route('/workers', methods=['POST', 'GET'])
def workers():
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    workers_list = Worker.query.order_by(Worker.id).all()
    jobs_list = Info.query.filter(Info.type_id == 3).order_by(Info.id).all()
    if request.method == "POST":
        name = request.form.get('name')
        surname = request.form.get('surname')
        job_id = request.form.get('job_id')
        text = request.form.get('text')
        img = request.files['img']
        if img:
            filename = secure_filename(img.filename)
            img_url = "/static/img/workers/" + filename
            app.config['UPLOADED_FOLDER'] = "static/img/workers"
            img.save(os.path.join(app.config['UPLOADED_FOLDER'], img.filename))
            add_info = Worker(name=name, info_id=job_id, text=text, img=img_url, surname=surname)
            add_info.add()
        else:
            add_info = Worker(name=name, info_id=job_id, text=text, surname=surname)
            add_info.add()
        return redirect(url_for('workers'))
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    return render_template('workers/index.html', workers_list=workers_list, jobs=jobs, jobs_list=jobs_list,
                           about_us=about_us, about_id=about_id, news=news, user=user)


@app.route('/edit_worker/<int:worker_id>', methods=['POST'])
def edit_worker(worker_id):
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    name = request.form.get('name')
    surname = request.form.get('surname')
    job_id = request.form.get('job_id')
    text = request.form.get('text')

    img = request.files['img']
    if img:
        worker = Info.query.filter(Worker.id == worker_id).first()
        types = Info.query.filter(Worker.img == worker.img, Worker.id != worker.id).first()
        if not types and worker.img:
            if os.path.isfile(worker.img[1:]):
                os.remove(worker.img[1:])
        filename = secure_filename(img.filename)
        img_url = "/static/img/workers/" + filename
        app.config['UPLOADED_FOLDER'] = "static/img/workers"

        img.save(os.path.join(app.config['UPLOADED_FOLDER'], img.filename))
        Worker.query.filter(Worker.id == worker_id).update({
            "name": name,
            "surname": surname,
            "text": text,
            "img": img_url,
            "info_id": job_id
        })
        db.session.commit()
    else:
        Worker.query.filter(Worker.id == worker_id).update({
            "name": name,
            "surname": surname,
            "text": text,
            "info_id": job_id
        })
        db.session.commit()
    return redirect(url_for('workers'))


@app.route('/delete_worker/<int:worker_id>')
def delete_worker(worker_id):
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    Worker.query.filter(Worker.id == worker_id).delete()
    db.session.commit()
    return redirect(url_for('workers'))


@app.route('/workers_front')
def workers_front():
    workers_list = Worker.query.order_by(Worker.id).all()
    return render_template('front/workers/teacher.html', workers_list=workers_list)
