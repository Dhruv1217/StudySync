# StudySync ⚡

## Description
StudySync is a comprehensive, Flask-based Web Application designed as a Student Productivity Management System. It helps students track their tasks, calculate attendance, manage their CGPA, and monitor their overall study progress.

## Features
- **Authentication**: Create Account, Login, Change Password
- **Task Management**: Add, View, Edit, Complete, and Delete tasks (CRUD)
- **Attendance Calculator**: Track attended vs total classes to maintain >75%
- **CGPA Calculator**: Input semester SGPAs to calculate cumulative GPA
- **Study Progress**: Visual dashboard of overall academic performance
- **Weekly Report**: Summary of pending tasks and current stats

## Technologies Used
- **Backend Framework**: Python (Flask)
- **Database**: SQLAlchemy (SQLite for local development, PostgreSQL for Production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Templating Engine**: Jinja2
- **Production Server**: Gunicorn

## Project Structure

```text
StudySync/
│
├── app.py                  # Main Flask application logic and routing
├── models.py               # SQLAlchemy database schemas
├── requirements.txt        # Python dependencies
├── seed_db.py              # Script to initialize and seed the database
│
├── static/                 # Static assets
│   ├── css/styles.css
│   └── js/main.js
│
├── templates/              # HTML Templates (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── tasks.html
│   ├── attendance.html
│   ├── cgpa.html
│   ├── profile.html
│   ├── progress.html
│   ├── report.html
│   ├── login.html
│   ├── signup.html
│   └── change_password.html
│
└── .gitignore
```

## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Dhruv1217/StudySync.git
   cd StudySync
   ```

2. **Install Dependencies:**
   Make sure you have Python installed. It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the Database:**
   Run the seed script to create the local `studysync.db` SQLite database file.
   ```bash
   python seed_db.py
   ```

4. **Start the Development Server:**
   ```bash
   python app.py
   ```
   *The application will be running at `http://localhost:5000`*

## Deployment (Render)

This application is ready to be deployed on Render as a Web Service.

- **Environment:** `Python`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

*Note: For production, it is highly recommended to attach a free PostgreSQL database to your Render service and add its connection string as the `DATABASE_URL` environment variable.*
https://studysync-cvjr.onrender.com/