from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
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
    
    # Use lambda with timezone.utc for default database timestamps
    borrow_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    due_date = db.Column(db.DateTime, nullable=False)
    returned = db.Column(db.Boolean, default=False)

    def calculate_fine(self, fine_per_day=10):
        current_time = datetime.now(timezone.utc)
        # Ensure comparison works safely if existing database records are naive or aware
        due_date_aware = self.due_date if self.due_date.tzinfo else self.due_date.replace(tzinfo=timezone.utc)
        
        if not self.returned and current_time > due_date_aware:
            overdue_days = (current_time - due_date_aware).days
            return overdue_days * fine_per_day
        return 0