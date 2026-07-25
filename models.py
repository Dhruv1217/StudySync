from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    
    roll_number = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Relationships
    tasks = db.relationship('Task', backref='student', lazy=True, cascade="all, delete-orphan")
    attendance = db.relationship('Attendance', backref='student', uselist=False, cascade="all, delete-orphan")
    cgpa_record = db.relationship('CGPA', backref='student', uselist=False, cascade="all, delete-orphan")

    def __init__(self, roll_number=None, name=None, branch=None, semester=None, email=None, password=None, **kwargs):
        super().__init__(**kwargs)
        self.roll_number = roll_number
        self.name = name
        self.branch = branch
        self.semester = semester
        self.email = email
        self.password = password

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(50), db.ForeignKey('students.roll_number'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="Pending")

    def __init__(self, id=None, roll_number=None, title=None, subject=None, priority=None, due_date=None, status="Pending", **kwargs):
        super().__init__(**kwargs)
        if id is not None:
            self.id = id
        self.roll_number = roll_number
        self.title = title
        self.subject = subject
        self.priority = priority
        self.due_date = due_date
        self.status = status

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(50), db.ForeignKey('students.roll_number'), nullable=False, unique=True)
    total_classes = db.Column(db.Integer, default=0)
    attended_classes = db.Column(db.Integer, default=0)
    attendance_percentage = db.Column(db.Float, default=0.0)

    def __init__(self, id=None, roll_number=None, total_classes=0, attended_classes=0, attendance_percentage=0.0, **kwargs):
        super().__init__(**kwargs)
        if id is not None:
            self.id = id
        self.roll_number = roll_number
        self.total_classes = total_classes
        self.attended_classes = attended_classes
        self.attendance_percentage = attendance_percentage

class CGPA(db.Model):
    __tablename__ = 'cgpa_records'
    
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(50), db.ForeignKey('students.roll_number'), nullable=False, unique=True)
    semester_sgpa = db.Column(db.String(500), default="[]")  # Store list as JSON string
    cgpa = db.Column(db.Float, default=0.0)

    def __init__(self, id=None, roll_number=None, semester_sgpa="[]", cgpa=0.0, **kwargs):
        super().__init__(**kwargs)
        if id is not None:
            self.id = id
        self.roll_number = roll_number
        self.semester_sgpa = semester_sgpa
        self.cgpa = cgpa
