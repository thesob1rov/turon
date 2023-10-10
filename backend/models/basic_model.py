from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import *
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, functions

db = SQLAlchemy()


def db_setup(app):
    app.config.from_object('backend.models.config')
    db.app = app
    db.init_app(app)
    Migrate(app, db)
    return db


class User(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "user"
    username = Column(String)
    name = Column(String)
    surname = Column(String)
    image = Column(String)
    password = Column(String)
    role = Column(String)
    parent_name = Column(String)
    birth_date = Column(DateTime)
    number = Column(String)
    email = Column(String)
    address = Column(String)
    age = Column(String)
    teacher = db.relationship("Teacher", backref="user", order_by="Teacher.id")
    student = db.relationship("Student", backref="user", order_by="Student.id")
    pdf_contract = relationship("PdfContract", backref="user", order_by="PdfContract.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class Teacher(db.Model):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    subject_id = Column(Integer, ForeignKey("subject.id"))
    classes = relationship("Class", backref="teacher", secondary="teacher_class", order_by="Class.id")
    rooms = relationship("Room", backref="teacher", order_by="Room.id")
    flows = relationship("Flow", backref="teacher", order_by="Flow.id")
    daily_table = relationship("DailyTable", backref="teacher", order_by="DailyTable.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class Student(db.Model):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    class_number = Column(Integer, ForeignKey("class_type.id"))
    language_type = Column(Integer, ForeignKey("language.id"))
    classes = relationship("Class", backref="student", secondary="student_class", order_by="Class.id")
    student_month_payments = relationship("StudentMonthPayments", backref="student", order_by="StudentMonthPayments.id")
    student_month_in_payments = relationship("StudentPaymentsInMonth", backref="student",
                                             order_by="StudentPaymentsInMonth.id")
    student_discount = relationship("StudentDiscount", backref="student", order_by="StudentDiscount.id")
    deleted_student = relationship("DeletedStudent", backref="student", order_by="DeletedStudent.id")
    deleted_student_for_classes = relationship("DeletedStudentForClasses", backref="student",
                                               order_by="DeletedStudentForClasses.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class DeletedStudent(db.Model):
    __tablename__ = "deleted_student"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("student.id"))


class TypeInfo(db.Model):
    __tablename__ = "type_info"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    infos = relationship('Info', backref="type_info", order_by="Info.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class Info(db.Model):
    __tablename__ = "info"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    img = Column(String)
    type_id = Column(Integer, ForeignKey('type_info.id'))
    date = Column(DateTime)
    vacations = relationship("Vacation", backref="info", order_by="Vacation.id")
    workers = relationship("Worker", backref="info", order_by="Worker.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class Vacation(db.Model):
    __tablename__ = "vacation"
    id = Column(Integer, primary_key=True)
    info_id = Column(Integer, ForeignKey('info.id'))
    text = Column(String)
    requests = relationship("Requests", backref="vacation", order_by="Requests.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class Worker(db.Model):
    __tablename__ = "worker"
    id = Column(Integer, primary_key=True)
    info_id = Column(Integer, ForeignKey('info.id'))
    name = Column(String)
    surname = Column(String)
    img = Column(String)
    text = Column(String)

    def add(self):
        db.session.add(self)
        db.session.commit()


class Gallery(db.Model):
    __tablename__ = "gallery"
    id = Column(Integer, primary_key=True)
    img = Column(String)


class Partners(db.Model):
    __tablename__ = "partners"
    id = Column(Integer, primary_key=True)
    img = Column(String)


class Comments(db.Model):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    add_date = Column(DateTime)


class Requests(db.Model):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    phone = Column(String)
    vacation_id = Column(Integer, ForeignKey('vacation.id'))
    add_date = Column(DateTime)
    pdf_file = Column(String)

    def add(self):
        db.session.add(self)
        db.session.commit()


class Class(db.Model):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    class_number = Column(Integer)
    color = Column(String)
    price = Column(String)
    language_type = Column(Integer, ForeignKey("language.id"))
    deleted_student_for_classes = relationship("DeletedStudentForClasses", backref="class",
                                               order_by="DeletedStudentForClasses.id")
    deleted_classes = relationship("DeletedClasses", backref="class",
                                   order_by="DeletedClasses.id")
    subjects = relationship("Subject", backref="class", secondary="class_subjects",
                            order_by="Subject.id")
    daily_table = relationship("DailyTable", backref="class", order_by="DailyTable.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


db.Table('student_class',
         db.Column('class_id', db.Integer, db.ForeignKey('class.id')),
         db.Column('student_id', db.Integer, db.ForeignKey('student.id'))
         )

db.Table('teacher_class',
         db.Column('class_id', db.Integer, db.ForeignKey('class.id')),
         db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'))
         )


class Subject(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "subject"
    name = Column(String)
    teacher = relationship("Teacher", backref="subject", order_by="Teacher.id")
    flows = relationship("Flow", backref="subject", order_by="Flow.id")
    daily_table = relationship("DailyTable", backref="subject",
                               order_by="DailyTable.id")


db.Table('class_subjects',
         db.Column('class_id', db.Integer, db.ForeignKey('class.id')),
         db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'))
         )


class PdfContract(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "pdf_contract"
    user_id = Column(Integer, ForeignKey("user.id"))
    pdf = Column(String)


class AccountType(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "account_type"
    name = Column(String)
    student_month_payments = relationship("StudentMonthPayments", backref="account_type",
                                          order_by="StudentMonthPayments.id")
    student_payments_in_month = relationship("StudentPaymentsInMonth", backref="account_type",
                                             order_by="StudentPaymentsInMonth.id")
    overhead = relationship("Overhead", backref="account_type",
                            order_by="Overhead.id")


class StudentMonthPayments(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "student_month_payments"
    student_id = Column(Integer, ForeignKey("student.id"))
    account_type_id = Column(Integer, ForeignKey("account_type.id"))
    class_price = Column(Integer)
    payed = Column(Integer)
    another = Column(Integer)
    month = Column(DateTime)
    real_price = Column(Integer)
    discount_percentage = Column(Integer)
    student_payments_in_month = relationship("StudentPaymentsInMonth", backref="student_month_payments",
                                             order_by="StudentPaymentsInMonth.id")


class LanguageType(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "language"
    name = Column(String)
    student = relationship("Student", backref="language",
                           order_by="Student.id")
    classes = relationship("Class", backref="language",
                           order_by="Class.id")


class StudentPaymentsInMonth(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "student_payments_in_month"
    student_month_payments_id = Column(Integer, ForeignKey("student_month_payments.id"))
    student_id = Column(Integer, ForeignKey("student.id"))
    account_type_id = Column(Integer, ForeignKey("account_type.id"))
    payed = Column(Integer)
    date = Column(DateTime)


class Overhead(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "over_head"
    name = Column(String)
    account_type_id = Column(Integer, ForeignKey("account_type.id"))
    payed = Column(Integer)
    date = Column(DateTime)
    deleted_over_head = relationship("DeleteDOverhead", backref="over_head",
                                     order_by="DeleteDOverhead.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


class DeleteDOverhead(db.Model):
    __tablename__ = "deleted_over_head"
    id = Column(Integer, primary_key=True)
    over_head_id = Column(Integer, ForeignKey("over_head.id"))
    date = Column(DateTime)

    def add(self):
        db.session.add(self)
        db.session.commit()


class ClassType(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "class_type"
    class_number = Column(Integer)
    price = Column(Integer)
    student = relationship("Student", backref="class_type",
                           order_by="Student.id")


class DiscountType(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "discount_type"
    name = Column(String)
    student_discount = relationship("StudentDiscount", backref="discount_type",
                                    order_by="StudentDiscount.id")


class StudentDiscount(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "student_discount"
    student_id = Column(Integer, ForeignKey("student.id"))
    discount_type_id = Column(Integer, ForeignKey("discount_type.id"))
    discount_percentage = Column(Integer)


class DeletedStudentForClasses(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "deleted_student_for_classes"
    student_id = Column(Integer, ForeignKey("student.id"))
    class_id = Column(Integer, ForeignKey("class.id"))
    reason = Column(String)


class DeletedClasses(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "deleted_classes"
    class_id = Column(Integer, ForeignKey("class.id"))


class Room(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "room"
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    chair_count = Column(Integer)
    image = Column(String)
    daily_table = relationship("DailyTable", backref="room",
                               order_by="DailyTable.id")


class Flow(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "flow"
    name = Column(String)
    subject_id = Column(Integer, ForeignKey("subject.id"))
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    students = relationship("Student", secondary="flow_students", backref="room",
                            order_by="Student.id")


db.Table("flow_students",
         Column("flow_id", Integer, ForeignKey("flow.id")),
         Column("student_id", Integer, ForeignKey("student.id"))
         )


class TimeList(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "time_list"
    lesson_count = Column(String)
    start = Column(String)
    end = Column(String)
    daily_time = relationship("DailyTable", backref="time_list",
                              order_by="DailyTable.id")


class TimeTableDay(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "time_table_day"
    name = Column(String)
    daily_table = relationship("DailyTable", backref="time_table_day",
                               secondary="time_table_day_lessons",
                               order_by="DailyTable.id", uselist=True)


class DailyTable(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "daily_table"
    lesson_time = Column(Integer, ForeignKey("time_list.id"))
    room_id = Column(Integer, ForeignKey("room.id"))
    class_id = Column(Integer, ForeignKey("class.id"))
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    flow_id = Column(Integer, ForeignKey("flow.id"))
    subject_id = Column(Integer, ForeignKey("subject.id"))
    day_id = Column(Integer)
    flow_lesson = Column(Boolean)


db.Table("time_table_day_lessons",
         Column("time_table_day_id", Integer, ForeignKey("time_table_day.id")),
         Column("daily_table_id", Integer, ForeignKey("daily_table.id"))
         )
