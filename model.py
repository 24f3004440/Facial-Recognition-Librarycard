from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    face_encodings = db.Column(db.PickleType, nullable=False)  # Stores the facial embedding array (2 or more pics)
    borrow_records = db.relationship('BorrowRecord', backref='student', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    borrow_records = db.relationship('BorrowRecord', backref='book', lazy=True)

class BorrowRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    due_date = db.Column(db.DateTime, nullable=False)
    returned = db.Column(db.Boolean, default=False)

    def calculate_fine(self, fine_per_day=10):
        #Calculates overdue fine
        if not self.returned and datetime.datetime.now(datetime.UTC) > self.due_date:
            overdue_days = (datetime.datetime.now(datetime.UTC) - self.due_date).days
            return overdue_days * fine_per_day
        return 0