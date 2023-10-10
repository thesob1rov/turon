from app import *
from pathlib import Path
from docxtpl import DocxTemplate
import datetime


def pdf_folder():
    upload_folder = "static/pdf_contract/"
    return upload_folder


def docx_folder():
    upload_folder = "static/docx_contract/"
    return upload_folder


@app.route('/create_contract/<int:student_id>', methods=["POST", "GET"])
def create_contract(student_id):
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    student = User.query.filter(User.id == student_id).first()
    if not user:
        return redirect(url_for('home'))
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    document_path = Path(__file__).parent / "primary_shartnoma.docx"
    doc = DocxTemplate(document_path)
    if request.method == "POST":
        student_name = f'{student.name} {student.surname}'
        name = request.form.get("name")
        surname = request.form.get("surname")
        father_name = request.form.get("parent_name")
        parent = f'{name} {surname} {father_name}'
        passport = request.form.get("passport_seria")
        location_get = request.form.get("get_location")
        today = datetime.datetime.today()
        location = request.form.get("address")
        context = {
            "NAME": student_name,
            "PARENT": parent,
            "PASSPORT": passport,
            "LOCATIONGET": location_get,
            "TODAY": today.strftime("%Y-%m-%d"),
            "LOCATION": location
        }
        doc.render(context)
        folder = docx_folder()
        app.config['UPLOAD_FOLDER'] = folder
        doc.save(os.path.join(app.config['UPLOAD_FOLDER'], f"{student.name} {student.surname}-contract.docx"))
        return redirect(
            url_for("download", filename=f"static\\docx_contract\\{student.name} {student.surname}-contract.docx"))
    return render_template('contract/contract.html', about_us=about_us, news=news, jobs=jobs, about_id=about_id,
                           user=user, student=student)


@app.route('/download/<path:filename>')
def download(filename):
    return send_file(filename, as_attachment=True)
