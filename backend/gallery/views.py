from app import *
from backend.models.basic_model import *


@app.route('/gallery_edit/<int:id>', methods=['POST', 'GET'])
def gallery_edit(id):
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    photo = request.files.get('file')
    folder = "static/img/gallery"
    if photo and checkFile(photo.filename):
        photo_file = secure_filename(photo.filename)
        photo_url = "/" + folder + "/" + photo_file
        app.config['UPLOAD_FOLDER'] = folder
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
        Gallery.query.filter(Gallery.id == id).update({
            "img": photo_url
        })
        db.session.commit()
    gallery = Gallery.query.order_by(Gallery.id).all()
    gallery_list = []
    for img in gallery:
        info = {
            "id": img.id,
            "img_url": img.img
        }
        gallery_list.append(info)
    return jsonify({
        "success": True,
        "gallery_list": gallery_list
    })


@app.route('/gallery')
def gallery():
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    firstgallerylist = ["/static/img/photo_2023-03-14_15-24-26.jpg",
                        "/static/img/photo_2023-03-14_15-24-27.jpg",
                        "/static/img/photo_2023-03-14_15-24-28.jpg",
                        "/static/img/photo_2023-03-14_15-24-29.jpg",
                        "/static/img/photo_2023-03-14_15-24-32.jpg",
                        "/static/img/photo_2023-03-14_15-24-34.jpg",
                        "/static/img/photo_2023-03-14_15-24-36.jpg",
                        "/static/img/photo_2023-03-14_15-24-38.jpg",
                        "/static/img/photo_2023-03-14_15-24-27%20(2).jpg"
                        ]
    # for item in firstgallerylist:
    #     filter_img = Gallery.query.filter(Gallery.img == item).first()
    #     if not filter_img:
    #         add = Gallery(img=item)
    #         db.session.add(add)
    #         db.session.commit()
    gallery = Gallery.query.order_by(Gallery.id).all()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    return render_template('gallery/index.html', gallery=gallery, about_id=about_id, about_us=about_us, news=news,
                           jobs=jobs, user=user)


@app.route('/get_gallery')
def get_gallery():
    gallery = Gallery.query.order_by(Gallery.id).all()
    gallery_list = []
    for img in gallery:
        info = {
            "id": img.id,
            "img_url": img.img
        }
        gallery_list.append(info)
    return jsonify({
        "success": True,
        "gallery_list": gallery_list
    })


@app.route('/get_partners')
def get_partners():
    gallery = Partners.query.order_by(Partners.id).all()
    gallery_list = []
    for img in gallery:
        info = {
            "id": img.id,
            "img_url": img.img
        }
        gallery_list.append(info)
    return jsonify({
        "success": True,
        "gallery_list": gallery_list
    })


@app.route('/partners')
def partners():
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    firstgallerylist = ["/static/img/photo_2023-03-14_15-24-26.jpg",
                        "/static/img/photo_2023-03-14_15-24-27.jpg",
                        "/static/img/photo_2023-03-14_15-24-28.jpg",
                        "/static/img/photo_2023-03-14_15-24-29.jpg",
                        "/static/img/photo_2023-03-14_15-24-32.jpg"
                        ]
    # for item in firstgallerylist:
    #     filter_img = Partners.query.filter(Partners.img == item).first()
    #     if not filter_img:
    #         add = Partners(img=item)
    #         db.session.add(add)
    #         db.session.commit()
    partners = Partners.query.order_by(Partners.id).all()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    return render_template("partners/index.html", partners=partners, about_us=about_us, news=news, jobs=jobs,
                           about_id=about_id, user=user)


@app.route('/partner_edit/<int:id>', methods=['POST', 'GET'])
def partner_edit(id):

    user = current_user()
    if not user:
        return redirect(url_for('home'))
    photo = request.files.get('file')
    folder = "static/img/partners"
    if photo and checkFile(photo.filename):
        photo_file = secure_filename(photo.filename)
        photo_url = "/" + folder + "/" + photo_file
        app.config['UPLOAD_FOLDER'] = folder
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
        Partners.query.filter(Partners.id == id).update({
            "img": photo_url
        })
        db.session.commit()
    gallery = Partners.query.order_by(Partners.id).all()
    gallery_list = []
    for img in gallery:
        info = {
            "id": img.id,
            "img_url": img.img
        }
        gallery_list.append(info)
    return jsonify({
        "success": True,
        "gallery_list": gallery_list
    })
