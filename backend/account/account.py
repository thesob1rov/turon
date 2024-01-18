from app import *
from backend.settings.settings import *
from datetime import datetime
from flask_paginate import Pagination, get_page_args


def delete_payments():
    deleted_overheads = DeleteDOverhead.query.all()
    for deleted_overhead in deleted_overheads:
        dl_overhead = DeleteDOverhead.query.filter(DeleteDOverhead.id == deleted_overhead.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()
    overheads = Overhead.query.all()
    for overhead in overheads:
        dl_overhead = Overhead.query.filter(Overhead.id == overhead.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()
    student_payments_in_months = StudentPaymentsInMonth.query.all()
    for student_payments_in_month in student_payments_in_months:
        dl_overhead = StudentPaymentsInMonth.query.filter(
            StudentPaymentsInMonth.id == student_payments_in_month.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()
    student_month_payments = StudentMonthPayments.query.all()
    for student_month_payment in student_month_payments:
        dl_overhead = StudentMonthPayments.query.filter(StudentMonthPayments.id == student_month_payment.id).first()
        db.session.delete(dl_overhead)
        db.session.commit()


@app.route('/collection')
def collection():
    """
    Front endga malumot yuboradigan app route
    :return:
    """
    # delete_payments()
    error = check_session()
    if error:
        return redirect(url_for('home'))
    user = User.query.filter(User.id == 1).first()
    about_us = Info.query.filter(Info.type_id == 1).order_by(Info.id).first()
    about_id = 0
    about_us = TypeInfo.query.filter(TypeInfo.id == 1).first()
    news = TypeInfo.query.filter(TypeInfo.id == 2).first()
    jobs = TypeInfo.query.filter(TypeInfo.id == 3).first()
    about = Info.query.filter(Info.type_id == about_us.id).order_by(Info.id).first()
    payments = StudentPaymentsInMonth.query.order_by(StudentPaymentsInMonth.id).all()
    cost_all = Overhead.query.order_by(Overhead.id).all()
    balance = 0
    for payment in payments:
        balance += int(payment.payed)
    return render_template('account/account.html', payments=payments, cost_all=cost_all, user=user, about_us=about_us,
                           about_id=about_id, news=news,
                           jobs=jobs, about=about, balance=balance)


@app.route('/search', methods=['POST'])
def search():
    """
    Kunlar bo'yicha qidiarigan app route
    :return:
    """
    input_one = request.get_json()["input_one"]
    input_two = request.get_json()["input_two"]
    button = request.get_json()["button"]
    button_number = 0

    if button == 'Bank':
        button_number = 1
    elif button == 'Click':
        button_number = 2
    elif button == 'Cash':
        button_number = 3

    payment_all = StudentPaymentsInMonth.query.order_by(StudentPaymentsInMonth.id).all()
    cost_all = Overhead.query.order_by(Overhead.id).all()
    list_pay = []
    list_cost = []
    if button_number:
        for payment in payment_all:
            if payment.account_type_id == button_number and input_one[0:4] <= payment.date.strftime("%Y") and input_one[
                                                                                                              5:7] <= payment.date.strftime(
                "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[0:4] >= payment.date.strftime(
                "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[8:10] >= payment.date.strftime(
                "%d"):
                list_pay.append(payment.id)
        for cost in cost_all:
            if cost.account_type_id == button_number and input_one[0:4] <= cost.date.strftime("%Y") and input_one[
                                                                                                        5:7] <= cost.date.strftime(
                "%m") and input_one[8:10] <= cost.date.strftime("%d") and input_two[0:4] >= cost.date.strftime(
                "%Y") and input_two[5:7] >= cost.date.strftime("%m") and input_two[8:10] >= cost.date.strftime(
                "%d"):
                list_cost.append(cost.id)
    else:
        for payment in payment_all:
            if input_one[0:4] <= payment.date.strftime("%Y") and input_one[5:7] <= payment.date.strftime(
                    "%m") and input_one[8:10] <= payment.date.strftime("%d") and input_two[
                                                                                 0:4] >= payment.date.strftime(
                "%Y") and input_two[5:7] >= payment.date.strftime("%m") and input_two[8:10] >= payment.date.strftime(
                "%d"):
                list_pay.append(payment.id)
        for cost in cost_all:
            if input_one[0:4] <= cost.date.strftime("%Y") and input_one[5:7] <= cost.date.strftime(
                    "%m") and input_one[8:10] <= cost.date.strftime("%d") and input_two[
                                                                              0:4] >= cost.date.strftime(
                "%Y") and input_two[5:7] >= cost.date.strftime("%m") and input_two[8:10] >= cost.date.strftime(
                "%d"):
                list_cost.append(cost.id)
    payments = StudentPaymentsInMonth.query.filter(
        StudentPaymentsInMonth.id.in_([item for item in list_pay])).order_by(
        StudentPaymentsInMonth.id).all()
    cost_all_filter = Overhead.query.filter(Overhead.id.in_([item for item in list_cost])).order_by(Overhead.id).all()
    list_pay_fetch = []
    list_cost_fetch = []
    for pay in payments:
        info = {
            "id": pay.student_id,
            "name": pay.student.user.name,
            "surname": pay.student.user.surname,
            "payed": pay.payed,
            "account_type_name": pay.account_type.name,
            "date": pay.date.strftime("%Y-%m-%d")
        }
        list_pay_fetch.append(info)
    for cost in cost_all_filter:
        info = {
            "id": cost.id,
            "name": cost.name,
            "payed": cost.payed,
            "account_type_name": cost.account_type.name,
            "date": cost.date.strftime("%Y-%m-%d")
        }
        list_cost_fetch.append(info)
    balance = 0
    for payment in payments:
        balance += int(payment.payed)
    for cost in cost_all_filter:
        balance -= int(cost.payed)
    return jsonify({
        'payments': list_pay_fetch,
        'cost': list_cost_fetch,
        'balance': balance
    })
