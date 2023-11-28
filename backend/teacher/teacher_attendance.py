from app import *
from backend.settings.settings import *
from datetime import datetime
import calendar
from backend.teacher.teacher_salarys import *


@app.route('/teacher_attendance', methods=["POST", "GET"])
def teacher_attendance():
    info = request.get_json()["info"]
    teacher_id = info["teacher_id"]
    year_id = info["year_id"]
    month_id = info["month_id"]
    day_id = info["day_id"]
    status = info["status"]
    now_attendance = TeacherAttendance.query.filter(TeacherAttendance.teacher_id == int(teacher_id),
                                                    TeacherAttendance.year_id == int(year_id),
                                                    TeacherAttendance.month_id == int(month_id),
                                                    TeacherAttendance.day_id == int(day_id)).first()
    if not now_attendance:
        add_attendance = TeacherAttendance(teacher_id=teacher_id, year_id=year_id, month_id=month_id, day_id=day_id,
                                           status=status)
        add_attendance.add()
        calculate_teacher_salary()
        return jsonify("keldi")
    else:
        return jsonify("bu kunda davomat qilingan")
