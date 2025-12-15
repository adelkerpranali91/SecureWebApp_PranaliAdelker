
S.H.E.I.L.D. (Secure Hospital Engagement Interface for Login and Data) is a secure web-based hospital appointment system that is developed to ensure the protection of sensitive healthcare information and to eliminate typical web application attacks. The system allows many user roles and controls strict access to make sure that users can only access data and functionality that they are supposed to see. Security was considered an essential design requirement and was incorporated throughout the application lifecycle.

USER ROLES
- PATIENT --> REGISTER AND LOGIN
     USER can create, view, update and delete the appointment created.

- DOCTOR --> REGISTER AND LOGIN
     VIEW the appointments that are assigned to them.

RUNNING APPLICATION
PREREQUISITES
- Python 
- pip package manager
WINDOWS POWERSHELL - for secure version
- $env:SEC_KEY="your-secret-key"
RUN APPLICATION
- python app.py

TECHNOLOGY USED 
- Backend: Python (Flask)
- Frontend: HTML, CSS (Jinja2 templates)
- Database: SQLite
- Security Libraries: -->bcrypt – secure password hashing
                    -->Flask-WTF – CSRF protection
- Testing: Bandit (SAST)

FEATURES
- User registration and login
- Users : patient and doctor
- Appointment: create, view, editing and deletion
- Doctor can view appointment assigned to them

SECURITY OBJECTIVES
- Role BasedAccess Control to prevent unauthrrized appointment access
- Parameterized queries to prevent SQL injection attacks
- CSRF protection for state-changing request
- Secure configuration

USAGE GUIDELINES
- REGISTER NEW ACCOUNT AS PATIENT OR DOCTOR
- LOG IN USING CREDENTIALS
- PATIENTS --> CREATE, VIEW, EDIT AND DELETE
- DOCTOR --> VIEW APPOINTMENT ASSIGNED TO THEM
- SERVER SIDE BLOACK FOR UNAUTHORIZED ACTIONS

SECURITY IMPLEMENTED
- Password are hashed using bcrypt.
- Parameterized queries are used for all database interactions.
- Access is based on the user roles.
- POST request are enabled by CSRF tokens.
- Debug mode is disabled and secret key is loaded form enviroment.
- Session cookies configured with HttpOnly and SameSite.
  
TESTING
- STATIC APPLICATION SECURITY TESTING [SAST]
  Bandit - python SAST tool

  RESULT
  - Insecure version ---> hard-coded secret, SQL injection and enable debug
  - Secure version ---> No issues 

FILE STRUCTURE
SECUREWEB-INSECURE/
├── .vscode/
│   └── settings.json
├── models/
│   ├── __pycache__/
│   └── db_insecure.py
├── templates/
│   ├── appointments/
│   │   ├── booking.html
│   │   ├── delete.html
│   │   ├── edit.html
│   │   └── list.html
│   ├── auth/
│   │   ├── login.html
│   │   ├── register.html
│   ├── base.html
│   ├── dashboard.html
│   ├── index.html
├── app.py
└── clinic.db

SECUREWEB- SECURE/
├── .vscode/
│   └── settings.json
├── models/
│   ├── __pycache__/
│   └── db_insecure.py
├── templates/
│   ├── appointments/
│   │   ├── booking.html
│   │   ├── delete.html
│   │   ├── edit.html
│   │   └── list.html
│   ├── auth/
│   │   ├── login.html
│   │   ├── register.html
│   ├── base.html
│   ├── dashboard.html
│   ├── index.html
├── app.py
└── clinic.db




-----
PRANALI PRABHAKER ADELKER 
ID - 24203513
