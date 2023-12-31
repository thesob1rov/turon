from app import *
from backend.settings.settings import *
import calendar
from datetime import datetime
from backend.teacher.teacher_salarys import *

list_days = []


def get_calendar(current_year, next_year):
    calculate_teacher_salary()
    for year in range(current_year, next_year + 1):
        for month in range(1, 13):
            if (year == current_year and month not in [1, 2, 3, 4, 5, 6, 7, 8]) or (
                    year == next_year and month not in [9, 10, 11, 12]):
                month_name = calendar.month_name[month]
                object_days = {
                    'month_number': month,
                    'month_name': month_name,
                    'days': [],
                    'year': year
                }
                cal = calendar.monthcalendar(year, month)
                for week in cal:
                    for day in week:
                        day_str = str(day) if day != 0 else "  "
                        if day != 0:
                            if 1 <= day <= calendar.monthrange(year, month)[1]:
                                weeks_id = calendar.weekday(year, month, day)
                                day_name = calendar.day_name[weeks_id]
                            day_object = {
                                'day_number': day_str,
                                'day_name': day_name
                            }
                            object_days['days'].append(day_object)
                list_days.append(object_days)
    for year in list_days:
        year_b = Years.query.filter(Years.year == year["year"]).first()
        if not year_b:
            year_new = Years(year=year['year'])
            year_new.add()
        year_b = Years.query.filter(Years.year == year["year"]).first()
        if year_b:
            month_b = Month.query.filter(Month.month_number == year['month_number'],
                                         Month.years_id == year_b.id).first()
            if not month_b:
                month = Month(month_number=year['month_number'], month_name=year['month_name'], years_id=year_b.id)
                month.add()
                month_one = Month.query.filter(Month.month_number == year['month_number']).first()
                for day in year['days']:
                    day_b = Day.query.filter(Day.day_number == day['day_number'], Day.month_id == month_one.id,
                                             Day.year_id == year_b.id).first()
                    if not day_b:

                        new_day = Day(day_number=day['day_number'], day_name=day['day_name'],
                                      month_id=month_one.id, year_id=year_b.id)

                        if day['day_name'] == 'Sunday':
                            new_day = Day(day_number=day['day_number'], day_name=day['day_name'],
                                          month_id=month_one.id, year_id=year_b.id, type_id=1)
                        else:
                            new_day = Day(day_number=day['day_number'], day_name=day['day_name'],
                                          month_id=month_one.id, year_id=year_b.id, type_id=2)
                        new_day.add()


@app.route('/calendar_year')
def calendar_year():
    get_calendar(datetime.now().year, datetime.now().year + 1)
    calculate_teacher_salary()
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    about_id = 0
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    types = TypeDay.query.order_by(TypeDay.id).all()
    calendar = []
    account_types = AccountType.query.all()
    month_all = Month.query.order_by(Month.id).all()
    for month in month_all:
        week_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        object = {
            'year': month.years.year,
            'month': month.month_name,
            'week': [],
        }
        week = []
        for name in week_name:
            day_first_name = None
            days = []
            for day in month.day:
                if day.day_name == name:
                    if day.day_number == 1:
                        day_first_name = day.day_name
                    if day.type_day:
                        day_object = {
                            'day_id': day.id,
                            'day_number': day.day_number,
                            'day_name': day.day_name[0:3],
                            'color': day.type_day.color
                        }
                        days.append(day_object)
                    else:
                        day_object = {
                            'day_id': day.id,
                            'day_number': day.day_number,
                            'day_name': day.day_name[0:3],
                            # 'color': day.type_day.color
                        }
                        days.append(day_object)

            if day_first_name != None:
                number = week_name.index(day_first_name)
                while number + 1 <= 7:
                    week.append(week_name[number])
                    number += 1
            if name in week:
                week_object = {
                    'day_name': name,
                    'week': name,
                    'days': days
                }
                object['week'].append(week_object)
            else:
                week_object = {
                    'day_name': name,
                    'days': days
                }
                object['week'].append(week_object)
        calendar.append(object)
    return render_template('calendar/index.html', user=user, about_us=about_us, calendar_all=calendar, types=types,
                           about_id=about_id, news=news,
                           jobs=jobs, about=about,
                           account_types=account_types, month_all=month_all)


@app.route('/change_type', methods=['POST'])
def change_type():
    day_id = request.get_json()['day_id']
    type_id = request.get_json()['type_id']
    Day.query.filter(Day.id == day_id).update({
        'type_id': type_id
    })
    db.session.commit()
    color = TypeDay.query.filter(TypeDay.id == type_id).first().color

    return jsonify({
        'color': color
    })
