from app import *
from backend.settings.settings import *
from datetime import datetime
from flask_paginate import Pagination, get_page_args


@app.route('/collection', defaults={'type_request': "sp"})
@app.route('/collection/<type_request>/')
def collection(type_request):
    """
    Front endga malumot yuboradigan app route
    :return:
    """
    error = check_session()
    # if error:
    #     return redirect(url_for('home'))
    user = User.query.filter(User.id == 1).first()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    cost_all = Overhead.query.filter(Overhead.deleted_over_head == None).order_by(Overhead.id).all()
    student_pay_all = StudentPaymentsInMonth.query.order_by(StudentPaymentsInMonth.id).all()
    teacher_sal_all = GivenSalariesInMonth.query.order_by(GivenSalariesInMonth.id).all()
    worker_sal_all = WorkerSalaryInDay.query.filter(WorkerSalaryInDay.deleted_worker_salary_inDay == None).order_by(
        WorkerSalaryInDay.id).all()
    balance_sp = 0
    balance_ts = 0
    balance_ws = 0
    balance_co = 0
    for payment in student_pay_all:
        balance_sp += int(payment.payed)
    for payment in teacher_sal_all:
        balance_ts += int(payment.salary)
    for payment in worker_sal_all:
        balance_ws += int(payment.salary)
    for payment in cost_all:
        balance_co += int(payment.payed)
    balance = balance_sp - balance_ts - balance_ws - balance_co
    if type_request == 'sp' or type_request == '':
        payments = student_pay_all
    elif type_request == 'ts':
        payments = teacher_sal_all
    elif type_request == 'ws':
        payments = worker_sal_all
    elif type_request == 'co':
        payments = cost_all
    else:
        payments = []
        balance = 0
    return render_template('account/account.html', balance_sp=balance_sp, balance_ts=balance_ts, balance_ws=balance_ws,
                           balance_co=balance_co,
                           type_request=type_request, payments=payments,
                           user=user, about_us=about_us,
                           about_id=about_id, news=news,
                           jobs=jobs, about=about, balance=balance)


@app.route('/del_pay', methods=["POST"])
def del_pay():
    button_id = request.get_json()["button_id"]
    type_request = request.get_json()["type_request"]
    payments = []
    date = datetime.now()
    if type_request == 'sp' or type_request == '':
        object = StudentPaymentsInMonth.query.filter(StudentPaymentsInMonth.id == button_id).first()
        # del = DeletedWorkerSalaryInDay
        payments = []
    elif type_request == 'ws':
        object = WorkerSalaryInDay.query.filter(WorkerSalaryInDay.id == button_id).first()
        del_object = DeletedWorkerSalaryInDay(worker_salary_in_day_id=object.id, date=date)
        del_object.add()
        objects = WorkerSalaryInDay.query.filter(WorkerSalaryInDay.deleted_worker_salary_inDay == None).order_by(
            WorkerSalaryInDay.id).all()
        for object in objects:
            info = {
                "name": object.worker_salary.worker.user.name,
                "surname": object.worker_salary.worker.user.surname,
                "payed": object.salary,
                "account_type_name": object.account_type.name,
                "date": f' {object.years.year} -{object.month.month_number}-{object.day.day_number}'
            }
            payments.append(info)
    elif type_request == 'co':
        object = Overhead.query.filter(Overhead.id == button_id).first()
        del_object = DeleteDOverhead(over_head_id=object.id, date=date)
        del_object.add()
        objects = Overhead.query.filter(Overhead.deleted_over_head == None).order_by(Overhead.id).all()
        for object in objects:
            info = {
                "name": object.worker_salary.worker.user.name,
                "surname": object.worker_salary.worker.user.surname,
                "payed": object.salary,
                "account_type_name": object.account_type.name,
                "date": f' {object.years.year} -{object.month.month_number}-{object.day.day_number}'
            }
            payments.append(info)

    return jsonify({
        'payments': payments
    })


@app.route('/search', methods=["POST"])
def search():
    """
    Kunlar bo'yicha qidiarigan app route
    :return:
    """
    input_one = request.get_json()["input_one"]
    input_two = request.get_json()["input_two"]
    type_request = request.get_json()["type_request"]
    button = request.get_json()["button"]
    if button == 'Bank':
        button_number = 1
    elif button == 'Click':
        button_number = 2
    elif button == 'Cash':
        button_number = 3
    else:
        button_number = 0
    payment_all = StudentPaymentsInMonth.query.order_by(StudentPaymentsInMonth.id).all()
    cost_all = Overhead.query.filter(Overhead.deleted_over_head == None).order_by(Overhead.id).all()
    worker_salary_all = WorkerSalaryInDay.query.filter(WorkerSalaryInDay.deleted_worker_salary_inDay == None).order_by(
        WorkerSalaryInDay.id).all()
    teacher_salary_all = GivenSalariesInMonth.query.order_by(GivenSalariesInMonth.id).all()
    list_pay = []
    balance = 0
    if button_number != 0 and input_one and input_two:
        if type_request == 'sp' or type_request == '':
            for payment in payment_all:
                if payment.account_type_id == button_number and input_one[0:4] <= payment.date.strftime(
                        "%Y") and input_one[5:7] <= payment.date.strftime(
                    "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                 0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.student_id,
                        "name": payment.student.user.name,
                        "surname": payment.student.user.surname,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 'ws':
            for payment in worker_salary_all:
                if payment.account_type_id == button_number and int(input_one[0:4]) <= payment.years.year and int(
                        input_one[5:7]) <= payment.month.month_number and int(input_one[
                                                                              8:10]) <= payment.day.day_number and int(
                    input_two[
                    0:4]) >= payment.years.year and int(input_two[
                                                        5:7]) >= payment.month.month_number and int(input_two[
                                                                                                    8:10]) >= payment.day.day_number:
                    info = {
                        "name": payment.worker_salary.worker.user.name,
                        "surname": payment.worker_salary.worker.user.surname,
                        "payed": payment.salary,
                        "account_type_name": payment.account_type.name,
                        "date": f' {payment.years.year} -{payment.month.month_number}-{payment.day.day_number}'
                    }
                    balance += int(payment.salary)
                    list_pay.append(info)
        elif type_request == 'ts':
            for payment in teacher_salary_all:
                if payment.account_type_id == button_number and int(input_one[0:4]) <= payment.years.year and int(
                        input_one[5:7]) <= payment.month.month_number and int(input_one[
                                                                              8:10]) <= payment.day.day_number and int(
                    input_two[
                    0:4]) >= payment.years.year and int(input_two[
                                                        5:7]) >= payment.month.month_number and int(input_two[
                                                                                                    8:10]) >= payment.day.day_number:
                    info = {
                        "name": payment.teacher_salary.teacher.user.name,
                        "surname": payment.teacher_salary.teacher.user.surname,
                        "payed": payment.given_salary,
                        "account_type_name": payment.account_type.name,
                        "date": f' {payment.years.year} -{payment.month.month_number}-{payment.day.day_number}'
                    }
                    balance += int(payment.salary)
                    list_pay.append(info)
        elif type_request == 'co':
            for payment in cost_all:
                if payment.account_type_id == button_number and input_one[0:4] <= payment.date.strftime(
                        "%Y") and input_one[5:7] <= payment.date.strftime(
                    "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                 0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
    elif button_number == 0 and input_one != '' and input_two != '':
        if type_request == 'sp' or type_request == '':
            for payment in payment_all:
                if input_one[0:4] <= payment.date.strftime("%Y") and input_one[5:7] <= payment.date.strftime(
                        "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                     0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.student_id,
                        "name": payment.student.user.name,
                        "surname": payment.student.user.surname,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 'ws':
            for payment in worker_salary_all:
                if int(input_one[0:4]) <= payment.years.year and int(
                        input_one[5:7]) <= payment.month.month_number and int(input_one[
                                                                              8:10]) <= payment.day.day_number and int(
                    input_two[
                    0:4]) >= payment.years.year and int(input_two[
                                                        5:7]) >= payment.month.month_number and int(input_two[
                                                                                                    8:10]) >= payment.day.day_number:
                    info = {
                        "name": payment.worker_salary.worker.user.name,
                        "surname": payment.worker_salary.worker.user.surname,
                        "payed": payment.salary,
                        "account_type_name": payment.account_type.name,
                        "date": f' {payment.years.year} -{payment.month.month_number}-{payment.day.day_number}'
                    }
                    balance += int(payment.salary)
                    list_pay.append(info)
        elif type_request == 'ts':
            for payment in teacher_salary_all:
                if int(input_one[0:4]) <= payment.years.year and int(
                        input_one[5:7]) <= payment.month.month_number and int(input_one[
                                                                              8:10]) <= payment.day.day_number and int(
                    input_two[
                    0:4]) >= payment.years.year and int(input_two[
                                                        5:7]) >= payment.month.month_number and int(input_two[
                                                                                                    8:10]) >= payment.day.day_number:
                    info = {
                        "name": payment.teacher_salary.teacher.user.name,
                        "surname": payment.teacher_salary.teacher.user.surname,
                        "payed": payment.given_salary,
                        "account_type_name": payment.account_type.name,
                        "date": f' {payment.years.year} -{payment.month.month_number}-{payment.day.day_number}'
                    }
                    balance += int(payment.salary)
                    list_pay.append(info)
        elif type_request == 'co':
            for payment in cost_all:
                if input_one[0:4] <= payment.date.strftime("%Y") and input_one[5:7] <= payment.date.strftime(
                        "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                     0:4] >= payment.date.strftime(
                    "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[
                                                                                8:10] >= payment.date.strftime(
                    "%d"):
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
    elif button_number != 0 and input_one == None and input_two == None:
        if type_request == 'sp' or type_request == '':
            for payment in payment_all:
                if payment.account_type_id == button_number:
                    info = {
                        "id": payment.student_id,
                        "name": payment.student.user.name,
                        "surname": payment.student.user.surname,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
        elif type_request == 'ws':
            for payment in worker_salary_all:
                if payment.account_type_id == button_number:
                    info = {
                        "name": payment.worker_salary.worker.user.name,
                        "surname": payment.worker_salary.worker.user.surname,
                        "payed": payment.salary,
                        "account_type_name": payment.account_type.name,
                        "date": f' {payment.years.year} -{payment.month.month_number}-{payment.day.day_number}'
                    }
                    balance += int(payment.salary)
                    list_pay.append(info)
        elif type_request == 'ts':
            for payment in teacher_salary_all:
                if payment.account_type_id == button_number:
                    info = {
                        "name": payment.teacher_salary.teacher.user.name,
                        "surname": payment.teacher_salary.teacher.user.surname,
                        "payed": payment.given_salary,
                        "account_type_name": payment.account_type.name,
                        "date": f' {payment.years.year} -{payment.month.month_number}-{payment.day.day_number}'
                    }
                    balance += int(payment.salary)
                    list_pay.append(info)
        elif type_request == 'co':
            for payment in cost_all:
                if payment.account_type_id == button_number:
                    info = {
                        "id": payment.id,
                        "name": payment.name,
                        "payed": payment.payed,
                        "account_type_name": payment.account_type.name,
                        "date": payment.date.strftime("%Y-%m-%d")
                    }
                    balance += int(payment.payed)
                    list_pay.append(info)
    return jsonify({
        'payments': list_pay,
        'balance': balance
    })
