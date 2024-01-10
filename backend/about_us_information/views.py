from app import *
from backend.settings.settings import *
from datetime import datetime
import calendar


def about_us_information_images_folder():
    upload_folder = "static/about_us_information_images/"
    return upload_folder


@app.route('/staffing')
def staffing():
    user = current_user()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    staffings = Staffing.query.all()
    return render_template("staffing/staffing.html", about_us=about_us, news=news,
                           jobs=jobs,
                           about_id=about_id, user=user, staffings=staffings)


@app.route('/add_staffing', methods=["POST", "GET"])
def add_staffing():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            add = Staffing(title=title, content=content, img=photo_url)
            db.session.add(add)
            db.session.commit()
        else:
            add = Staffing(title=title, content=content)
            db.session.add(add)
            db.session.commit()
    return redirect(url_for("staffing"))


@app.route('/edit_staffing/<staffing_id>', methods=["POST", "GET"])
def edit_staffing(staffing_id):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            Staffing.query.filter(Staffing.id == staffing_id).update({
                "title": title,
                "content": content,
                "img": photo_url
            })
            db.session.commit()
        else:
            Staffing.query.filter(Staffing.id == staffing_id).update({
                "title": title,
                "content": content
            })
            db.session.commit()
    return redirect(url_for("staffing"))


@app.route('/delete_staffing/<staffing_id>', methods=["POST", "GET"])
def delete_staffing(staffing_id):
    staffing_info = Staffing.query.filter(Staffing.id == staffing_id).first()
    db.session.delete(staffing_info)
    db.session.commit()
    return redirect(url_for("staffing"))


@app.route('/premises')
def premises():
    user = current_user()

    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    premises = Premises.query.all()
    return render_template("premises/premises.html", about_us=about_us, news=news,
                           jobs=jobs,
                           about_id=about_id, user=user, premises=premises)


@app.route('/add_premises', methods=["POST", "GET"])
def add_premises():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            add = Premises(title=title, content=content, img=photo_url)
            db.session.add(add)
            db.session.commit()
        else:
            add = Premises(title=title, content=content)
            db.session.add(add)
            db.session.commit()
    return redirect(url_for("premises"))


@app.route('/edit_premises/<int:premises_id>', methods=["POST", "GET"])
def edit_premises(premises_id):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            Premises.query.filter(Premises.id == premises_id).update({
                "title": title,
                "content": content,
                "img": photo_url
            })
            db.session.commit()
        else:
            Premises.query.filter(Premises.id == premises_id).update({
                "title": title,
                "content": content
            })
            db.session.commit()
    return redirect(url_for("premises"))


@app.route('/delete_premises/<int:premises_id>', methods=["POST", "GET"])
def delete_premises(premises_id):
    premise = Premises.query.filter(Premises.id == premises_id).first()
    db.session.delete(premise)
    db.session.commit()
    return redirect(url_for("premises"))


@app.route('/community_and_partnership', methods=["POST", "GET"])
def community_and_partnership():
    user = current_user()

    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    community_and_partnerships = CommunityAndHomePartnership.query.all()
    return render_template("community_and_parentship/community.html", about_us=about_us, news=news,
                           jobs=jobs,
                           about_id=about_id, user=user, community_and_partnerships=community_and_partnerships)


@app.route('/add_community_and_partnership', methods=["POST", "GET"])
def add_community_and_partnership():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            add = CommunityAndHomePartnership(title=title, content=content, img=photo_url)
            db.session.add(add)
            db.session.commit()
        else:
            add = CommunityAndHomePartnership(title=title, content=content)
            db.session.add(add)
            db.session.commit()
    return redirect(url_for("community_and_partnership"))


@app.route('/edit_community_and_partnership/<int:community_and_partnership_id>', methods=["POST", "GET"])
def edit_community_and_partnership(community_and_partnership_id):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            CommunityAndHomePartnership.query.filter(
                CommunityAndHomePartnership.id == community_and_partnership_id).update({
                "title": title,
                "content": content,
                "img": photo_url
            })
            db.session.commit()
        else:
            CommunityAndHomePartnership.query.filter(
                CommunityAndHomePartnership.id == community_and_partnership_id).update({
                "title": title,
                "content": content
            })
            db.session.commit()
    return redirect(url_for("community_and_partnership"))


@app.route('/delete_community_and_partnership/<int:community_and_partnership_id>', methods=["POST", "GET"])
def delete_community_and_partnership(community_and_partnership_id):
    premise = CommunityAndHomePartnership.query.filter(
        CommunityAndHomePartnership.id == community_and_partnership_id).first()
    db.session.delete(premise)
    db.session.commit()
    return redirect(url_for("community_and_partnership"))


@app.route('/student_learning_and_well_being', methods=["POST", "GET"])
def student_learning_and_well_being():
    user = current_user()

    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    student_learnings = StudentsLearningAndWellBeing.query.all()
    return render_template("student_learning_and_well_being/student_learning.html", about_us=about_us, news=news,
                           jobs=jobs,
                           about_id=about_id, user=user, student_learnings=student_learnings)


@app.route('/create_student_learning_and_well_being', methods=["POST", "GET"])
def create_student_learning_and_well_being():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            add = StudentsLearningAndWellBeing(title=title, content=content, img=photo_url)
            db.session.add(add)
            db.session.commit()
        else:
            add = StudentsLearningAndWellBeing(title=title, content=content)
            db.session.add(add)
            db.session.commit()
    return redirect(url_for("student_learning_and_well_being"))


@app.route('/edit_student_learning_and_well_being/<int:student_learning_and_well_being_id>', methods=["POST", "GET"])
def edit_student_learning_and_well_being(student_learning_and_well_being_id):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            StudentsLearningAndWellBeing.query.filter(
                StudentsLearningAndWellBeing.id == student_learning_and_well_being_id).update({
                "title": title,
                "content": content,
                "img": photo_url
            })
            db.session.commit()
        else:
            StudentsLearningAndWellBeing.query.filter(
                StudentsLearningAndWellBeing.id == student_learning_and_well_being_id).update({
                "title": title,
                "content": content
            })
            db.session.commit()
    return redirect(url_for("student_learning_and_well_being"))


@app.route('/delete_student_learning_and_well_being/<int:student_learning_and_well_being_id>', methods=["POST", "GET"])
def delete_student_learning_and_well_being(student_learning_and_well_being_id):
    student_learning_and_well_being = StudentsLearningAndWellBeing.query.filter(
        StudentsLearningAndWellBeing.id == student_learning_and_well_being_id).first()
    db.session.delete(student_learning_and_well_being)
    db.session.commit()
    return redirect(url_for("student_learning_and_well_being"))


@app.route('/teach_asses', methods=["POST", "GET"])
def teach_asses():
    user = current_user()

    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    teach_assesies = TeachAsses.query.all()
    return render_template("teaching_and_assesment/about.html", about_us=about_us, news=news, jobs=jobs,
                           about_id=about_id, user=user, teach_assesies=teach_assesies)


@app.route('/create_teach_asses', methods=["POST", "GET"])
def create_teach_asses():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            add = TeachAsses(title=title, content=content, img=photo_url)
            db.session.add(add)
            db.session.commit()
        else:
            add = TeachAsses(title=title, content=content)
            db.session.add(add)
            db.session.commit()
    return redirect(url_for("teach_asses"))


@app.route('/edit_teach_asses/<int:teach_asses_id>', methods=["POST", "GET"])
def edit_teach_asses(teach_asses_id):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            TeachAsses.query.filter(
                TeachAsses.id == teach_asses_id).update({
                "title": title,
                "content": content,
                "img": photo_url
            })
            db.session.commit()
        else:
            TeachAsses.query.filter(
                TeachAsses.id == teach_asses_id).update({
                "title": title,
                "content": content
            })
            db.session.commit()
    return redirect(url_for("teach_asses"))


@app.route('/delete_teach_asses/<int:teach_asses_id>', methods=["POST", "GET"])
def delete_teach_asses(teach_asses_id):
    teach_asses = TeachAsses.query.filter(
        TeachAsses.id == teach_asses_id).first()
    db.session.delete(teach_asses)
    db.session.commit()
    return redirect(url_for("teach_asses"))


@app.route('/purpose_direction', methods=["POST", "GET"])
def purpose_direction():
    user = current_user()

    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    purpose_directions = PurposeDirection.query.all()
    return render_template("purpose/purpose.html", about_us=about_us, news=news, jobs=jobs,
                           about_id=about_id, user=user, purpose_directions=purpose_directions)


@app.route('/create_purpose_direction', methods=["POST", "GET"])
def create_purpose_direction():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            add = PurposeDirection(title=title, content=content, img=photo_url)
            db.session.add(add)
            db.session.commit()
        else:
            add = PurposeDirection(title=title, content=content)
            db.session.add(add)
            db.session.commit()
    return redirect(url_for("purpose_direction"))


@app.route('/edit_purpose_direction/<int:purpose_direction_id>', methods=["POST", "GET"])
def edit_purpose_direction(purpose_direction_id):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            PurposeDirection.query.filter(
                PurposeDirection.id == purpose_direction_id).update({
                "title": title,
                "content": content,
                "img": photo_url
            })
            db.session.commit()
        else:
            PurposeDirection.query.filter(
                PurposeDirection.id == purpose_direction_id).update({
                "title": title,
                "content": content
            })
            db.session.commit()
    return redirect(url_for("purpose_direction"))


@app.route('/delete_purpose_direction/<int:purpose_direction_id>', methods=["POST", "GET"])
def delete_purpose_direction(purpose_direction_id):
    purpose_direction = PurposeDirection.query.filter(
        PurposeDirection.id == purpose_direction_id).first()
    db.session.delete(purpose_direction)
    db.session.commit()
    return redirect(url_for("purpose_direction"))


@app.route('/governance_ownership_leadership', methods=["POST", "GET"])
def governance_ownership_leadership():
    user = current_user()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    governances = GovernanceOwnershipLeadership.query.all()
    return render_template("governance/governance.html", about_us=about_us, news=news, jobs=jobs,
                           about_id=about_id, user=user, governances=governances)


@app.route('/create_governance_ownership_leadership', methods=["POST", "GET"])
def create_governance_ownership_leadership():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            add = GovernanceOwnershipLeadership(title=title, content=content, img=photo_url)
            db.session.add(add)
            db.session.commit()
        else:
            add = GovernanceOwnershipLeadership(title=title, content=content)
            db.session.add(add)
            db.session.commit()
    return redirect(url_for("governance_ownership_leadership"))


@app.route('/edit_governance_ownership_leadership/<int:governance_ownership_leadership_id>', methods=["POST", "GET"])
def edit_governance_ownership_leadership(governance_ownership_leadership_id):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            GovernanceOwnershipLeadership.query.filter(
                GovernanceOwnershipLeadership.id == governance_ownership_leadership_id).update({
                "title": title,
                "content": content,
                "img": photo_url
            })
            db.session.commit()
        else:
            GovernanceOwnershipLeadership.query.filter(
                GovernanceOwnershipLeadership.id == governance_ownership_leadership_id).update({
                "title": title,
                "content": content
            })
            db.session.commit()
    return redirect(url_for("governance_ownership_leadership"))


@app.route('/delete_governance_ownership_leadership/<int:governance_ownership_leadership_id>', methods=["POST", "GET"])
def delete_governance_ownership_leadership(governance_ownership_leadership_id):
    governance_ownership_leadership = GovernanceOwnershipLeadership.query.filter(
        GovernanceOwnershipLeadership.id == governance_ownership_leadership_id).first()
    db.session.delete(governance_ownership_leadership)
    db.session.commit()
    return redirect(url_for("governance_ownership_leadership"))


@app.route('/curriculum', methods=["POST", "GET"])
def curriculum():
    user = current_user()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    curriculums = Curriculum.query.all()
    return render_template("curriculum/currilculum.html", about_us=about_us, news=news, jobs=jobs,
                           about_id=about_id, user=user, curriculums=curriculums)


@app.route('/create_curriculum', methods=["POST", "GET"])
def create_curriculum():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            add = Curriculum(title=title, content=content, img=photo_url)
            db.session.add(add)
            db.session.commit()
        else:
            add = Curriculum(title=title, content=content)
            db.session.add(add)
            db.session.commit()
    return redirect(url_for("curriculum"))


@app.route('/edit_curriculum/<int:curriculum_id>', methods=["POST", "GET"])
def edit_curriculum(curriculum_id):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        photo = request.files["img"]
        folder = about_us_information_images_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_file))
            Curriculum.query.filter(
                Curriculum.id == curriculum_id).update({
                "title": title,
                "content": content,
                "img": photo_url
            })
            db.session.commit()
        else:
            Curriculum.query.filter(
                Curriculum.id == curriculum_id).update({
                "title": title,
                "content": content
            })
            db.session.commit()
    return redirect(url_for("curriculum"))


@app.route('/delete_curriculum/<int:curriculum_id>', methods=["POST", "GET"])
def delete_curriculum(curriculum_id):
    curriculum = Curriculum.query.filter(
        Curriculum.id == curriculum_id).first()
    db.session.delete(curriculum)
    db.session.commit()
    return redirect(url_for("curriculum"))


@app.route('/campus_life', methods=["POST", "GET"])
def campus_life():
    user = current_user()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    return render_template("campus_life/life.html", about_us=about_us, news=news, jobs=jobs,
                           about_id=about_id, user=user)


@app.route('/mock', methods=["POST", "GET"])
def mock():
    user = current_user()
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    if request.method == "POST":
        name = request.form.get("name")
        number = request.form.get("number")
        add = Clients(name=name, number=number)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for("mock"))
    return render_template("mock/mock.html", about_us=about_us, news=news, jobs=jobs,
                           about_id=about_id, user=user)
