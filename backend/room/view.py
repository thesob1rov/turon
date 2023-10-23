from app import *
from backend.settings.settings import *


@app.route('/rooms', methods=["POST", "GET"])
def rooms():
    """
    xonalini page
    :return:
    """
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

    teachers = Teacher.query.all()
    rooms = Room.query.all()
    return render_template('rooms/xona.html', about_us=about_us, news=news, jobs=jobs, about_id=about_id,
                           user=user, teachers=teachers, rooms=rooms)


@app.route('/creat_room', methods=["POST", "GET"])
def creat_room():
    """
    xona yaratish
    :return:
    """
    if request.method == "POST":
        name = request.form.get("name")
        teacher_id = request.form.get("teacher_id")
        chair_count = request.form.get("count")
        photo = request.files["photo"]
        if photo:
            filename = secure_filename(photo.filename)
            img_url = "/static/img/rooms/" + filename
            app.config['UPLOADED_FOLDER'] = "static/img/rooms"
            photo.save(os.path.join(app.config['UPLOADED_FOLDER'], photo.filename))
            add = Room(name=name, teacher_id=teacher_id, chair_count=chair_count, image=img_url)
            db.session.add(add)
            db.session.commit()
        else:
            add = Room(name=name, teacher_id=teacher_id, chair_count=chair_count)
            db.session.add(add)
            db.session.commit()
        return redirect(url_for('rooms'))
    return redirect(url_for("rooms"))


@app.route('/room_profile/<int:room_id>', methods=["POST", "GET"])
def room_profile(room_id):
    """
    xonani profili
    :param room_id: kirilgan xonani id si
    :return:
    """
    room = Room.query.filter(Room.id == room_id).first()
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
    teachers = Teacher.query.all()
    return render_template("room_profile/room.html", about_us=about_us, news=news, jobs=jobs, about_id=about_id,
                           user=user, room=room, teachers=teachers)


@app.route('/edit_room/<int:room_id>', methods=["POST", "GET"])
def edit_room(room_id):
    """
    xonani profili
    :param room_id: kirilgan xonani id si
    :return:
    """
    if request.method == "POST":
        name = request.form.get("name")
        teacher_id = request.form.get("teacher_id")
        chair_count = request.form.get("count")
        photo = request.files["photo"]
        if photo:
            filename = secure_filename(photo.filename)
            img_url = "/static/img/rooms/" + filename
            app.config['UPLOADED_FOLDER'] = "static/img/rooms"
            photo.save(os.path.join(app.config['UPLOADED_FOLDER'], photo.filename))
            Room.query.filter(Room.id == room_id).update({
                "name": name,
                "teacher_id": teacher_id,
                "chair_count": chair_count,
                "image": img_url
            })
            db.session.commit()
        else:
            Room.query.filter(Room.id == room_id).update({
                "name": name,
                "teacher_id": teacher_id,
                "chair_count": chair_count
            })
            db.session.commit()
    return redirect(url_for('room_profile', room_id=room_id))


@app.route('/delete_room/<int:room_id>', methods=["POST", "GET"])
def delete_room(room_id):
    """
    xonani ochirish
    :param room_id: tanlangan xonani id si
    :return:
    """
    delete_room = Room.query.filter(Room.id == room_id).first()
    db.session.delete(delete_room)
    db.session.commit()
    return redirect(url_for('rooms'))
