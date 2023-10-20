from flask import *
from backend.models.basic_model import *
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from pprint import pprint
import requests

link = 'https://turonedu.uz/'

# from backend.settings.settings import *

app = Flask(__name__)
app.config.from_object('backend.models.config')
db = db_setup(app)
migrate = Migrate(app, db)


def check_session():
    user = current_user()
    error = False
    # print(user.id)
    try:
        if not user and user.role != "admin":
            error = True
            return error
    except AttributeError:
        error = True
        return error


from backend.base_route.views import *
from backend.about_us_jobs.views import *
from backend.news.views import *
from backend.vacation.views import *
from backend.workers.views import *
from backend.gallery.views import *
from backend.student.routes import *
from backend.teacher.routes import *
from backend.sinf.routes import *
from backend.subjects.views import *
from backend.contract.views import *
from backend.account.payment import *
from backend.room.view import *
from backend.timetable.view import *
from backend.teacher.teacher_salarys import *

if __name__ == '__main__':
    app.run()
