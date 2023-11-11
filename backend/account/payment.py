import requests

from app import *
from backend.settings.settings import *
from datetime import datetime
from flask_paginate import Pagination, get_page_args
import string


@app.route('/add_payment/<int:student_id>', methods=["POST", "GET"])
def add_payment(student_id):
    error = check_session()
    if error:
        return redirect(url_for('home'))
    today = datetime.today()
    datem = datetime(today.year, today.month, 1)
    user = current_user()
    student = Student.query.filter(Student.id == student_id).first()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    about_id = 0
    if about:
        about_id = about.id
    account_types = AccountType.query.all()

    return render_template('account/payment.html', user=user, about_us=about_us, about_id=about_id, news=news,
                           jobs=jobs, about=about, account_types=account_types, student=student)


@app.route('/payment', methods=["POST", "GET"])
def payment():
    today = datetime.today()
    date = datetime(today.year, today.month, today.day)
    # data_object = datetime.datetime.strptime(date, '%m-%d-%Y')
    info = request.get_json()["info"]
    student_id = info["student_id"]
    money = info["money"]
    account_type_id = info["account_type_id"]
    student_mont_payments = StudentMonthPayments.query.filter(StudentMonthPayments.student_id == student_id,
                                                              StudentMonthPayments.another > 0).order_by(
        StudentMonthPayments.id).all()
    get_money = money
    money_another = 0
    for student_mont_payment in student_mont_payments:
        student = Student.query.filter(Student.id == student_mont_payment.student_id).first()
        if student.student_discount:
            result = int(student_mont_payment.class_price) / 100 * int(student.student_discount[0].discount_percentage)
            discounted_price = int(student_mont_payment.class_price) - result
            StudentMonthPayments.query.filter(StudentMonthPayments.student_id == student_mont_payment.student_id,
                                              StudentMonthPayments.id == student_mont_payment.id,
                                              StudentMonthPayments.another == student_mont_payment.class_price).update({
                "class_price": int(discounted_price),
                "another": int(discounted_price),
                "real_price": int(student_mont_payment.class_price),
                "discount_percentage": int(student.student_discount[0].discount_percentage)
            })
            db.session.commit()
        if int(student_mont_payment.another) < int(get_money):

            get_money = int(get_money) - int(student_mont_payment.another)
            StudentMonthPayments.query.filter(StudentMonthPayments.student_id == student_mont_payment.student_id,
                                              StudentMonthPayments.id == student_mont_payment.id).update({
                "payed": student_mont_payment.class_price,
                "another": 0,
                "account_type_id": account_type_id
            })
            db.session.commit()
            add = StudentPaymentsInMonth(student_id=student_mont_payment.student_id,
                                         student_month_payments_id=student_mont_payment.id,
                                         payed=int(get_money), date=date,
                                         account_type_id=account_type_id)
            db.session.add(add)
            db.session.commit()
        else:
            another = int(student_mont_payment.another) - int(get_money)
            StudentMonthPayments.query.filter(StudentMonthPayments.student_id == student_mont_payment.student_id,
                                              StudentMonthPayments.id == student_mont_payment.id,
                                              StudentMonthPayments.another > 0).update({
                "payed": int(get_money) + int(student_mont_payment.payed),
                "another": another,
                "account_type_id": account_type_id
            })
            db.session.commit()
            add = StudentPaymentsInMonth(student_id=student_mont_payment.student_id,
                                         student_month_payments_id=student_mont_payment.id,
                                         payed=int(get_money), date=date, account_type_id=account_type_id)
            db.session.add(add)
            db.session.commit()
            filtered_payed = StudentMonthPayments.query.filter(
                StudentMonthPayments.student_id == student_mont_payment.student_id,
                StudentMonthPayments.id == student_mont_payment.id,
                StudentMonthPayments.another == 0).first()
            if filtered_payed:
                StudentMonthPayments.query.filter(StudentMonthPayments.student_id == student_mont_payment.student_id,
                                                  StudentMonthPayments.id == student_mont_payment.id,
                                                  StudentMonthPayments.another == 0).update({
                    "payed": student_mont_payment.class_price
                })
                db.session.commit()
            break
    return jsonify()


@app.route('/student_payment_list/<int:student_id>', methods=["POST", "GET"])
def student_payment_list(student_id):
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    student_payments = StudentMonthPayments.query.filter(StudentMonthPayments.student_id == student_id).order_by(
        StudentMonthPayments.id).all()
    student = Student.query.filter(Student.id == student_id).first()
    return render_template("student_payed_list/to'lov.html", user=user, about_us=about_us, about_id=about_id, news=news,
                           jobs=jobs, about=about, pages=student_payments, student=student)


@app.route('/student_payment_in_month/<int:month_payment_id>', methods=["POST", "GET"])
def student_payment_in_month(month_payment_id):
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    student_payments = StudentPaymentsInMonth.query.filter(
        StudentPaymentsInMonth.student_month_payments_id == month_payment_id).all()
    return render_template('student_payment_in_month/student_payment_in_month.html', user=user, about_us=about_us,
                           about_id=about_id, news=news,
                           jobs=jobs, about=about, pages=student_payments)


def calc(months, years, days):
    balance = 0
    cash = 0
    bank = 0
    click = 0
    payments_in_pay = StudentPaymentsInMonth.query.order_by(StudentPaymentsInMonth.id).all()
    cash_payments_in_pay = StudentPaymentsInMonth.query.filter(StudentPaymentsInMonth.account_type_id == 3).all()
    bank_payments_in_pay = StudentPaymentsInMonth.query.filter(StudentPaymentsInMonth.account_type_id == 1).all()
    click_payments_in_pay = StudentPaymentsInMonth.query.filter(StudentPaymentsInMonth.account_type_id == 2).all()
    payments_in_cost = Overhead.query.order_by(Overhead.id, Overhead.deleted_over_head == None).all()
    cash_payments_in_cost = Overhead.query.filter(Overhead.account_type_id == 3,
                                                  Overhead.deleted_over_head == None).all()
    bank_payments_in_cost = Overhead.query.filter(Overhead.account_type_id == 1,
                                                  Overhead.deleted_over_head == None).all()
    click_payments_in_cost = Overhead.query.filter(Overhead.account_type_id == 2,
                                                   Overhead.deleted_over_head == None).all()
    payments_in_salary = Teacher_salary_day.query.order_by(Teacher_salary_day.id).all()
    cash_payments_in_salary = Teacher_salary_day.query.filter(Teacher_salary_day.account_type_id == 3).order_by(
        Teacher_salary_day.id).all()
    bank_payments_in_salary = Teacher_salary_day.query.filter(Teacher_salary_day.account_type_id == 1).order_by(
        Teacher_salary_day.id).all()
    click_payments_in_salary = Teacher_salary_day.query.filter(Teacher_salary_day.account_type_id == 2).order_by(
        Teacher_salary_day.id).all()

    for payment in payments_in_pay:
        balance += int(payment.payed)
    for cash_payment in cash_payments_in_pay:
        cash += int(cash_payment.payed)
    for bank_payment in bank_payments_in_pay:
        bank += int(bank_payment.payed)
    for click_payment in click_payments_in_pay:
        click += int(click_payment.payed)

    for payment in payments_in_cost:
        balance -= int(payment.payed)
    for cash_payment in cash_payments_in_cost:
        cash -= int(cash_payment.payed)
    for bank_payment in bank_payments_in_cost:
        bank -= int(bank_payment.payed)
    for click_payment in click_payments_in_cost:
        click -= int(click_payment.payed)

    for payment in payments_in_salary:
        balance -= int(payment.salary)
    for cash_payment in cash_payments_in_salary:
        cash -= int(cash_payment.salary)
    for bank_payment in bank_payments_in_salary:
        bank -= int(bank_payment.salary)
    for click_payment in click_payments_in_salary:
        click -= int(click_payment.salary)

    for payment in payments_in_pay:
        payment_date = payment.date.month
        if not payment_date in months:
            months.append(payment_date)
    for payment in payments_in_pay:
        payment_date = payment.date.year
        if not payment_date in years:
            years.append(payment_date)
    for payment in payments_in_pay:
        payment_date = payment.date.day
        if not payment_date in days:
            days.append(payment_date)
    return balance, cash, bank, click


@app.route('/add_cost', methods=['POST'])
def add_cost():
    today = datetime.today()
    date = datetime(today.year, today.month, today.day)
    name = string.capwords(request.form.get('name'))
    payeds = request.form.get('payed')
    payeds = payeds.split()
    payed_add = ''
    for payed in payeds:
        payed_add += str(payed)
    payed = int(payed_add)
    account_type_id = request.form.get('account_type_id')
    if name and payed and account_type_id:
        new_cost = Overhead(name=name, account_type_id=account_type_id, payed=payed, date=date)
        new_cost.add()
    return redirect(url_for('all_payments', type_request='cost', page_num=1))


@app.route('/all_payments', defaults={'type_request': "pay", 'page_num': 1}, methods=['POST', 'GET'])
@app.route('/all_payments/<type_request>/<int:page_num>', methods=["POST", "GET"])
def all_payments(type_request, page_num):
    error = check_session()
    # if error:
    #     return redirect(url_for('home'))
    user = User.query.first()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    payments = StudentPaymentsInMonth.query.order_by(StudentPaymentsInMonth.id).all()
    cash_payments = StudentPaymentsInMonth.query.filter(StudentPaymentsInMonth.account_type_id == 3).all()
    bank_payments = StudentPaymentsInMonth.query.filter(StudentPaymentsInMonth.account_type_id == 1).all()
    click_payments = StudentPaymentsInMonth.query.filter(StudentPaymentsInMonth.account_type_id == 2).all()
    account_types = AccountType.query.all()
    balance = 0
    cash = 0
    bank = 0
    click = 0
    years = []
    years.sort()
    months = []
    months.sort()
    days = []
    days.sort()
    balance, cash, bank, click = calc(months, years, days)
    if type_request == 'pay':
        payments = StudentPaymentsInMonth.query.paginate(per_page=5, page=page_num, error_out=True)
    elif type_request == 'cost':
        del_cost = DeleteDOverhead.query.order_by(DeleteDOverhead.id).all()
        payments = Overhead.query.filter(
            Overhead.deleted_over_head == None).paginate(per_page=5, page=page_num, error_out=True)
    elif type_request == 'salary':
        payments = Teacher_salary_day.query.paginate(per_page=5, page=page_num,
                                                     error_out=True)
    page_nex = page_num + 1
    page_prev = page_num - 1
    page_pres = page_num
    page_last = 0

    for list in payments.iter_pages():
        page = list
        page_last = page
    year_b = Years.query.order_by(Years.id).all()
    month_b = Month.query.order_by(Month.id).all()
    day_b = Day.query.order_by(Day.id).all()
    return render_template("all_payments/all_payments.html", payments=payments, user=user, about_us=about_us,
                           year_b=year_b, month_b=month_b, day_b=day_b,
                           about_id=about_id, news=news,
                           jobs=jobs, about=about, balance=balance, cash=cash, bank=bank, click=click,
                           account_types=account_types, months=months, years=years, days=days,
                           type_request=type_request, page_nex=page_nex, page_prev=page_prev, page_last=page_last,
                           page_pres=page_pres)


@app.route('/filter_payments', methods=["POST", "GET"])
def filter_payments():
    info = request.get_json()["info"]
    data = "2023-08"
    date = datetime.strptime(data, "%Y-%m")
    payments = StudentPaymentsInMonth.query.filter(StudentPaymentsInMonth.date == date).all()
    filtered_payments = []
    if info["account_type_id"] == "all":
        if info["year"] == "all":
            if info["month"] == "all":
                payments = StudentPaymentsInMonth.query.all()
                for payment in payments:
                    info = {
                        "name": payment.student.user.name,
                        "surname": payment.student.user.surname,
                        "payed": payment.payed,
                        "account_type": payment.student_month_payments.account_type.name,
                        "date": payment.date
                    }
                    filtered_payments.append(info)
            else:
                payments = StudentPaymentsInMonth.query.filter(
                    StudentPaymentsInMonth.date.strftime('%m') == int(info["month"])).all()
                for payment in payments:
                    info = {
                        "name": payment.student.user.name,
                        "surname": payment.student.user.surname,
                        "payed": payment.payed,
                        "account_type": payment.student_month_payments.account_type.name,
                        "date": payment.date
                    }
                    filtered_payments.append(info)
        else:
            if info["month"] == "all":
                payments = StudentPaymentsInMonth.query.filter(
                    StudentPaymentsInMonth.date.strftime('%Y') == info["year"]).all()
                for payment in payments:
                    info = {
                        "name": payment.student.user.name,
                        "surname": payment.student.user.surname,
                        "payed": payment.payed,
                        "account_type": payment.student_month_payments.account_type.name,
                        "date": payment.date
                    }
                    filtered_payments.append(info)
            else:
                payments = StudentPaymentsInMonth.query.filter(
                    StudentPaymentsInMonth.date.strftime('%Y') == info["year"],
                    StudentPaymentsInMonth.date.strftime('%m') == info["month"]).all()
                for payment in payments:
                    info = {
                        "name": payment.student.user.name,
                        "surname": payment.student.user.surname,
                        "payed": payment.payed,
                        "account_type": payment.student_month_payments.account_type.name,
                        "date": payment.date
                    }
                    filtered_payments.append(info)


    else:
        pass
        # if info["year"] == "all":
        #     if info["month"] == "all":
        #         if info["day"] == "all":
        #             payments = StudentPaymentsInMonth.query.filter(
        #                 StudentPaymentsInMonth.account_type_id == int(info["account_type_id"])).all()
        #             for payment in payments:
        #                 info = {
        #                     "name": payment.student.user.name,
        #                     "surname": payment.student.user.surname,
        #                     "payed": payment.payed,
        #                     "account_type": payment.student_month_payments.account_type.name,
        #                     "date": payment.date
        #                 }
        #                 filtered_payments.append(info)
        #         else:
        #             pass
    return jsonify()


@app.route('/discount/<int:student_id>', methods=["POST", "GET"])
def discount(student_id):
    student = Student.query.filter(Student.id == student_id).first()
    if request.method == "POST":
        discount_type = request.form.get("discount_type")
        percentage = request.form.get("percentage")
        if student.student_discount:
            filter_discount = StudentDiscount.query.filter(StudentDiscount.discount_type_id == discount_type,
                                                           StudentDiscount.student_id == student.id).first()
            if filter_discount:
                StudentDiscount.query.filter(StudentDiscount.discount_type_id == discount_type,
                                             StudentDiscount.student_id == student.id).update({
                    "discount_percentage": percentage
                })
                db.session.commit()
            else:
                add = StudentDiscount(discount_type_id=discount_type, student_id=student_id,
                                      discount_percentage=percentage)
                db.session.add(add)
                db.session.commit()
        else:
            add = StudentDiscount(discount_type_id=discount_type, student_id=student_id, discount_percentage=percentage)
            db.session.add(add)
            db.session.commit()
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = current_user()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    discount_types = DiscountType.query.all()
    return render_template('discount/discount.html', user=user, about_us=about_us,
                           about_id=about_id, news=news,
                           jobs=jobs, about=about, discount_types=discount_types, student=student)


@app.route('/check_discount', methods=["POST", "GET"])
def check_discount():
    info = request.get_json()["info"]
    student = Student.query.filter(Student.id == info["student_id"]).first()
    student_discount = StudentDiscount.query.filter(StudentDiscount.student_id == student.id,
                                                    StudentDiscount.discount_type_id == info["discount_type"])
    discount_percentage = 0
    if student_discount:
        for discount in student_discount:
            discount_percentage = discount.discount_percentage
    return jsonify({
        "percentage": discount_percentage
    })


@app.route('/delete_payment', methods=["POST", "GET"])
def delete_payment():
    id = request.get_json()["id"]
    student_payment_in_month = StudentPaymentsInMonth.query.filter(StudentPaymentsInMonth.id == id).first()
    month_payment = StudentMonthPayments.query.filter(
        StudentMonthPayments.id == student_payment_in_month.student_month_payments_id).first()
    StudentPaymentsInMonth.query.filter(StudentPaymentsInMonth.id == id).delete()
    db.session.commit()
    all_payments = StudentPaymentsInMonth.query.filter(
        StudentPaymentsInMonth.student_month_payments_id == month_payment.id).all()
    sum = 0
    for payment in all_payments:
        sum += int(payment.payed)
    another = int(month_payment.class_price) - int(sum)
    StudentMonthPayments.query.filter(
        StudentMonthPayments.id == month_payment.id).update({
        "payed": sum,
        "another": another,
    })
    db.session.commit()
    return jsonify()


@app.route('/delete_cost', methods=["POST", "GET"])
def delete_cost():
    id = request.get_json()["id"]
    today = datetime.today()
    date = datetime(today.year, today.month, today.day)
    del_cost = Overhead.query.filter(Overhead.id == id).first()
    cost = DeleteDOverhead(over_head_id=id, date=date)
    cost.add()
    return jsonify()


@app.route('/search_pay', methods=["POST", "GET"])
def search_pay():
    search = string.capwords(request.get_json()["search"])
    pays = db.session.query(Student).join(Student.user).options(contains_eager(Student.user)).filter(
        Student.student_month_payments != None,
        or_(User.name.like('%' + search + '%'))).order_by(Student.id).all()
    student_id_list = []
    filtered_pay = []
    for pay in pays:
        if pay.id not in student_id_list:
            student_id_list.append(pay.id)
    payments = StudentPaymentsInMonth.query.filter(
        StudentPaymentsInMonth.student_id.in_([item for item in student_id_list])).order_by(
        StudentPaymentsInMonth.id).all()
    for pay in payments:
        info = {
            "id": pay.student_id,
            "name": pay.student.user.name,
            "surname": pay.student.user.surname,
            "payed": pay.payed,
            "account_type_name": pay.account_type.name,
            "date": pay.date.strftime("%Y-%m-%d")
        }
        filtered_pay.append(info)
    return jsonify({
        "filtered_pay": filtered_pay
    })


@app.route('/search_cost', methods=["POST", "GET"])
def search_cost():
    search = string.capwords(request.get_json()["search"])
    cost_all = Overhead.query.filter(Overhead.name.like('%' + search + '%'),
                                     Overhead.deleted_over_head == None).order_by(Overhead.id).all()
    filtered_cost = []
    for cost in cost_all:
        info = {
            "id": cost.id,
            "name": cost.name,
            "payed": cost.payed,
            "account_type_name": cost.account_type.name,
            "date": cost.date.strftime("%Y-%m-%d")
        }
        filtered_cost.append(info)
    return jsonify({
        "filtered_cost": filtered_cost
    })


@app.route('/filter_salary', methods=["POST", "GET"])
def filter_salary():
    button_id = request.get_json()["button_id"]
    salary_all = Teacher_salary_day.query.filter(Teacher_salary_day.account_type_id == button_id).order_by(
        Teacher_salary_day.id).all()
    filtered_salary = []
    for salary in salary_all:
        info = {
            'teacher_name': salary.teacher.user.name,
            'reason': salary.reason,
            'salary': salary.salary,
            'account_type': salary.account_type.name,
            'date': f' {salary.day.years.year} - {salary.day.month.month_number} - {salary.day.day_number} '
        }
        filtered_salary.append(info)
    return jsonify({
        'filtered_salary': filtered_salary
    })


@app.route('/filter_date', methods=["POST", "GET"])
def filter_date():
    year = request.get_json()["year"]
    month = request.get_json()["month"]
    day = request.get_json()["day"]
    print(year)
    print(month)
    print(day)
    if year:
        print(True)
        salary_all = db.session.query(Teacher_salary_day).join(Teacher_salary_day.day).options(
            contains_eager(Teacher_salary_day.day)).filter(Day.year_id == year).order_by(
            Teacher_salary_day.id).all()

        if month:
            print(month)
            salary_all = db.session.query(Teacher_salary_day).join(Teacher_salary_day.day).options(
                contains_eager(Teacher_salary_day.day)).filter(Day.year_id == year, Day.month_id == month).order_by(
                Teacher_salary_day.id).all()

            if day:
                print(day)
                salary_all = db.session.query(Teacher_salary_day).join(Teacher_salary_day.day).options(
                    contains_eager(Teacher_salary_day.day)).filter(Day.year_id == year, Day.month_id == month,
                                                                   Day.id == day).order_by(
                    Teacher_salary_day.id).all()
    elif not year and month and day:
        salary_all = db.session.query(Teacher_salary_day).join(Teacher_salary_day.day).options(
            contains_eager(Teacher_salary_day.day)).filter(Day.month_id == month, Day.id == day).order_by(
            Teacher_salary_day.id).all()
    elif year and not month and day:
        salary_all = db.session.query(Teacher_salary_day).join(Teacher_salary_day.day).options(
            contains_eager(Teacher_salary_day.day)).filter(Day.year_id == year, Day.id == day).order_by(
            Teacher_salary_day.id).all()
    elif not year and not day and month:
        salary_all = db.session.query(Teacher_salary_day).join(Teacher_salary_day.day).options(
            contains_eager(Teacher_salary_day.day)).filter(Day.month_id == month).order_by(
            Teacher_salary_day.id).all()
    elif not year and not month and day:
        salary_all = db.session.query(Teacher_salary_day).join(Teacher_salary_day.day).options(
            contains_eager(Teacher_salary_day.day)).filter(Day.id == day).order_by(
            Teacher_salary_day.id).all()

    filtered_salary = []
    for salary in salary_all:
        info = {
            'teacher_name': salary.teacher.user.name,
            'reason': salary.reason,
            'salary': salary.salary,
            'account_type': salary.account_type.name,
            'date': f' {salary.day.years.year} - {salary.day.month.month_number} - {salary.day.day_number} '
        }
        filtered_salary.append(info)
    return jsonify({
        'filtered_salary': filtered_salary
    })
