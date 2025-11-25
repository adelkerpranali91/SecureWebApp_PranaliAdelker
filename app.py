# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.db_insecure import (
    init_db,
    create_user,
    get_user_by_email,
    # appointment helpers
    create_appointment,
    get_all_appointments,
    get_appointment_by_id,
    update_appointment,
    delete_appointment,
)

app = Flask(__name__)
app.secret_key = "dev-insecure-secret"  # intentionally weak for insecure baseline

# Initialize DB at startup (creates tables if missing)
with app.app_context():
    init_db()


# -----------------------
# Index / home
# -----------------------
@app.route("/")
def index():
    if "email" in session:
        full_name = session.get("full_name", "")
        role = session.get("role", "")
        return render_template("index.html", full_name=full_name, role=role)
    return redirect(url_for("login"))


# -----------------------
# Dashboard (shows welcome cards AND inline appointment list)
# -----------------------
@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        flash("Please login first")
        return redirect(url_for("login"))

    # pull appointments to show on dashboard (insecure baseline: shows all)
    apts = get_all_appointments()

    return render_template(
        "dashboard.html",
        full_name=session.get("full_name", ""),
        role=session.get("role", ""),
        email=session.get("email", ""),
        appointments=apts
    )


# -----------------------
# Auth: Register / Login / Logout
# -----------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # collect fields
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm_password", "").strip()
        role = request.form.get("role", "patient")
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        dob = request.form.get("date_of_birth", "").strip()
        address = request.form.get("address", "").strip()
        emergency_name = request.form.get("emergency_name", "").strip()
        emergency_phone = request.form.get("emergency_phone", "").strip()
        insurance = request.form.get("insurance_number", "").strip()

        # simple server-side required checks (still insecure baseline overall)
        required = [email, password, confirm, full_name, phone, dob, address, emergency_name, emergency_phone]
        if any(not v for v in required):
            flash("Please fill all required fields (email, password, full name, phone, DOB, address, emergency contact).")
            return redirect(url_for("register"))
        if password != confirm:
            flash("Passwords do not match.")
            return redirect(url_for("register"))
        if get_user_by_email(email):
            flash("Email already registered.")
            return redirect(url_for("register"))

        # create user (INSECURE: plaintext password, raw SQL inside create_user)
        try:
            create_user(email, password, role, full_name, phone, dob, address, emergency_name, emergency_phone, insurance)
        except Exception as e:
            # rough error handling — keep simple for insecure baseline
            flash(f"Error creating user: {e}")
            return redirect(url_for("register"))

        flash("Registered (insecure). Please log in.")
        return redirect(url_for("login"))

    return render_template("auth/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        user = get_user_by_email(email)
        # INSECURE: plaintext password comparison
        if user and user.get("password") == password:
            # store useful fields in session
            session["email"] = user.get("email")
            session["full_name"] = user.get("full_name")
            session["role"] = user.get("role")
            flash("Logged in (insecure).")
            # redirect to dashboard per your request
            return redirect(url_for("dashboard"))

        flash("Invalid credentials")
        return redirect(url_for("login"))

    return render_template("auth/login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for("login"))


# -----------------------
# Appointments (insecure CRUD)
# -----------------------
@app.route("/appointments")
def appointments():
    # show the dashboard (which already contains the inline appointments list)
    if "email" not in session:
        flash("Please login first")
        return redirect(url_for("login"))
    # redirect to dashboard so list appears inline on same page
    return redirect(url_for("dashboard"))



@app.route("/appointments/create", methods=["GET", "POST"])
def create_appointment_view():
    if "email" not in session:
        flash("Please login first")
        return redirect(url_for("login"))

    if request.method == "POST":
        # patient display name taken from full_name in session
        patient_username = session.get("full_name", "")
        doctor_name = request.form.get("doctor_name", "").strip()
        date = request.form.get("date", "").strip()
        time = request.form.get("time", "").strip()
        reason = request.form.get("reason", "").strip()

        if not (patient_username and doctor_name and date and time):
            flash("Please fill required appointment fields.")
            return redirect(url_for("create_appointment_view"))

        # INSECURE: raw SQL via create_appointment (intentional)
        create_appointment(patient_username, doctor_name, date, time, reason)
        flash("Appointment created (insecure).")
        return redirect(url_for("dashboard"))  # return to dashboard so list shows inline

    # show form; it can prefill patient name
    return render_template("appointments/create.html", patient_name=session.get("full_name", ""))


@app.route("/appointments/edit/<int:apt_id>", methods=["GET", "POST"])
def edit_appointment_view(apt_id):
    if "email" not in session:
        flash("Please login first")
        return redirect(url_for("login"))

    apt = get_appointment_by_id(apt_id)
    if not apt:
        flash("Appointment not found")
        return redirect(url_for("dashboard"))

    # INSECURE: no authorization check (any logged-in user may edit any appointment)
    if request.method == "POST":
        patient_username = request.form.get("patient_username", apt["patient_username"])
        doctor_name = request.form.get("doctor_name", apt["doctor_name"])
        date = request.form.get("date", apt["date"])
        time = request.form.get("time", apt["time"])
        reason = request.form.get("reason", apt["reason"])

        update_appointment(apt_id, patient_username, doctor_name, date, time, reason)
        flash("Appointment updated (insecure).")
        return redirect(url_for("dashboard"))

    return render_template("appointments/edit.html", appointment=apt)


@app.route("/appointments/delete/<int:apt_id>", methods=["GET", "POST"])
def delete_appointment_view(apt_id):
    if "email" not in session:
        flash("Please login first")
        return redirect(url_for("login"))

    apt = get_appointment_by_id(apt_id)
    if not apt:
        flash("Appointment not found")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        # INSECURE: no RBAC check
        delete_appointment(apt_id)
        flash("Appointment deleted (insecure).")
        return redirect(url_for("dashboard"))

    return render_template("appointments/delete_confirm.html", appointment=apt)


# -----------------------
# Simple debug route to view current session (optional)
# -----------------------
@app.route("/whoami")
def whoami():
    if "email" in session:
        return {"email": session.get("email"), "full_name": session.get("full_name"), "role": session.get("role")}
    return {"logged_in": False}


if __name__ == "__main__":
    app.run(debug=True)
