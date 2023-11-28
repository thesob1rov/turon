from app import *
from backend.models.basic_model import *
from werkzeug.security import *


def current_user():
    get_user = None
    if 'username' in session:
        get_user = User.query.filter(User.username == session['username']).first()
        # get_user = User.query.filter(User.id == 10).first()
    return get_user


def create_menu():
    menu_list = ["Biz haqimizda", "Yangiliklar", "Lavozimlar"]
    for menu in menu_list:
        exist_menu = TypeInfo.query.filter(TypeInfo.name == menu).first()
        if not exist_menu:
            exist_menu = TypeInfo(name=menu)
            exist_menu.add()

    admin = User.query.filter(User.username == "admin", User.name == "admin", User.surname == "admin").first()
    if not admin:
        admin = User(username="admin", name="admin", surname="admin",
                     password=generate_password_hash("admin1234", method='scrypt'), role="admin")
        db.session.add(admin)
        db.session.commit()

    director = User.query.filter(User.username == "director", User.name == "director",
                                 User.surname == "director").first()
    if not director:
        director = User(username="director", name="director", surname="director",
                        password=generate_password_hash("max1234", method='scrypt'), role="director")
        db.session.add(director)
        db.session.commit()
