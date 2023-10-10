import calendar
from datetime import datetime
from app import *
from flask import jsonify
import os
from werkzeug.utils import secure_filename
import timedelta
from dateutil.rrule import rrule, DAILY
from datetime import date
from pprint import pprint


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}


def news_folder():
    upload_folder = 'static/img/news'
    return upload_folder


def checkFile(filename):
    value = '.' in filename
    type_file = filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return value and type_file


now = datetime.now()
year = now.year
month = now.month


def update_dates():
    global month, year
    now = datetime.now()
    year = now.year
    month = now.month


def fill():
    global month, year
    days = []
    month = int(month)
    info_label = calendar.month_name[month] + ', ' + str(year)

    month_days = calendar.monthrange(year, month)[1]
    info_date = info_label
    for n in range(month_days):
        if len(str(month)) == 1:
            month = "0" + str(month)
        rng = n + 1
        full_time = str(year) + '-' + f'{month}' + '-' + str(rng)
        filter_time = Info.query.filter(Info.date == full_time, Info.type_id == 2).all()
        info_days = {
            "day_range": rng,
            "boolean": False,
            "events": []
        }
        if filter_time:
            dates = []
            for time in filter_time:
                dates.append({
                    "id": time.id,
                    "title": time.title,
                    "img": time.img,
                    "desc": time.text,
                    "date": time.date.strftime("%d %B"),
                    "edit_date": time.date.strftime("%Y-%m-%d"),
                })
            info_days.update({
                "boolean": True,
                "events": dates
            })
        days.append(info_days)

    info = {
        "day": days,
        "info_date": info_date
    }
    return info


@app.route('/add_news/<int:type_id>', methods=['POST', 'GET'])
def add_news(type_id):
    user = current_user()
    error = check_session()
    if error:
        return redirect(url_for('home'))
    if request.method == "POST":
        name = request.form.get("add_name")
        desc = request.form.get("add_desc")
        date = request.form.get("add_date")
        photo = request.files['add_img']
        folder = news_folder()
        print(photo)
        if photo and checkFile(photo.filename):
            print(True)
            photo_file = secure_filename(photo.filename)
            photo_url = "/" + folder + "/" + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            add = Info(title=name, img=photo_url, text=desc, date=date, type_id=type_id)
            db.session.add(add)
            db.session.commit()
        else:
            add = Info(title=name, text=desc, date=date, type_id=type_id)
            db.session.add(add)
            db.session.commit()
        return redirect(url_for("calendar_info", type_id=type_id))


@app.route("/news", methods=["GET"])
def change_status():
    update_dates()
    return jsonify({
        "date": fill()
    })


@app.route("/edit_news/<int:info_id>", methods=["POST"])
def edit_news(info_id):

    user = current_user()
    error = check_session()
    if error:
        return redirect(url_for('home'))
    name = request.form.get("add_name")
    desc = request.form.get("add_desc")
    date = request.form.get("add_date")
    photo = request.files['add_img']
    folder = news_folder()
    info = Info.query.filter(Info.id == info_id).first()
    if photo and checkFile(photo.filename):
        info = Info.query.filter(Info.id == info_id).first()
        types = Info.query.filter(Info.img == info.img, Info.id != info.id).first()
        if not types and info.img:
            if os.path.isfile(info.img[1:]):
                os.remove(info.img[1:])
        photo_file = secure_filename(photo.filename)
        photo_url = "/" + folder + "/" + photo_file
        app.config['UPLOAD_FOLDER'] = folder
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
        Info.query.filter(Info.id == info_id).update({
            "title": name,
            "text": desc,
            "date": date,
            "img": photo_url
        })
        db.session.commit()
    Info.query.filter(Info.id == info_id).update({
        "title": name,
        "text": desc,
        "date": date,
    })
    db.session.commit()
    return redirect(url_for("calendar_info", type_id=info.type_id))


@app.route("/calendar_change/<num>", methods=["GET"])
def calendar_change(num):
    global month, year
    month = int(month)
    month += int(num)
    if month == 0:
        month = 12
        year -= 1
    if month == 13:
        month = 1
        year += 1

    return jsonify({
        "date": fill()
    })


@app.route('/calendar_info/<int:type_id>', methods=['GET'])
def calendar_info(type_id):
    user = current_user()
    error = check_session()
    if error:
        return redirect(url_for('home'))
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    return render_template('news/index.html', type_id=type_id, about_us=about_us, about_id=about_id, news=news,
                           jobs=jobs, user=user)


@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    Info.query.filter(Info.id == id).delete()
    db.session.commit()
    return redirect(url_for('calendar_info', type_id=2))


@app.route('/news_front')
def news_front():
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).order_by(TypeInfo.id).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    return render_template('front/news/index.html', about_id=about_id, about_us=about_us)
