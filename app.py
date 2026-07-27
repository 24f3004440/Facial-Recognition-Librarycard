import os
from flask import Flask, render_template, Response, jsonify
from models import db, Student, BorrowRecord
import cv2
from utils import recognize_face_from_frame

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/students'

db.init_app(app)

with app.app_context():
    db.create_all()

camera = cv2.VideoCapture(0)
latest_frame = None

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    global latest_frame

    while True:
        success, frame = camera.read()

        if not success:
            break

        latest_frame = frame.copy()

        ret, buffer = cv2.imencode('.jpg', frame)

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            buffer.tobytes() +
            b'\r\n'
        )

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/scan_face', methods=['POST'])
def scan_face():
    global latest_frame

    if latest_frame is None:
        return jsonify({
            'status': 'error',
            'message': 'No camera frame available.'
        })

    frame = latest_frame.copy()

    students = Student.query.all()
    matched_student = recognize_face_from_frame(frame, students)

    if matched_student:
        active_records = BorrowRecord.query.filter_by(
            student_id=matched_student.id,
            returned=False
        ).all()

        books_data = []
        total_fine = 0

        for record in active_records:
            fine = record.calculate_fine()
            total_fine += fine

            books_data.append({
                'title': record.book.title,
                'author': record.book.author,
                'borrow_date': record.borrow_date.strftime('%Y-%m-%d'),
                'due_date': record.due_date.strftime('%Y-%m-%d'),
                'fine': fine
            })

        return jsonify({
            'status': 'success',
            'student_name': matched_student.name,
            'roll_number': matched_student.roll_number,
            'books': books_data,
            'total_fine': total_fine
        })

    return jsonify({
        'status': 'not_found',
        'message': 'Face not recognized. Please register.'
    })

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=False)