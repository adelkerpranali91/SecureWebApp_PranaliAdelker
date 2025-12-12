#SECURE DB_INSECURE.PY
import sqlite3
from typing import List, Dict

import bcrypt

DB_PATH = "clinic.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    
    conn = get_conn()
    cur = conn.cursor()

    #CREATE USER TABLE - PASSWORD AS PLAINTEXT
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'patient',full_name TEXT NOT NULL,phone TEXT NOT NULL,date_of_birth TEXT NOT NULL, 
        address TEXT NOT NULL,emergency_name TEXT NOT NULL,emergency_phone TEXT NOT NULL,insurance_number TEXT);
    """)

    # CREATE APPOINTMENTS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,patient_username TEXT NOT NULL,doctor_name TEXT NOT NULL,
        date TEXT NOT NULL,time TEXT NOT NULL,reason TEXT,created_at TEXT DEFAULT (datetime('now')));
    """)
    conn.commit()
    conn.close()
    
def hash_password(plain_password: str) -> str:
     hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
     return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except:
        return False


# CREATING USER
def create_user(email: str, password: str, role: str = "patient",
                full_name: str = "", phone: str = "", date_of_birth: str = "",
                address: str = "", emergency_name: str = "", emergency_phone: str = "",
                insurance_number: str = ""):

    conn = get_conn()
    cur = conn.cursor()
    #PARAMERIZED QUERY - PLACEHOLDER
    sql = """
        INSERT INTO users (
            email, password, role, full_name, phone, date_of_birth,
            address, emergency_name, emergency_phone, insurance_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    hashed = hash_password(password)
    cur.execute(sql, (
        email, hashed, role, full_name, phone, date_of_birth,
        address, emergency_name, emergency_phone, insurance_number
    ))

    conn.commit()
    conn.close()

def get_user_by_email(email: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()

    conn.close()
    return dict(row) if row else None

def get_password_hash_by_email(email: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    return row["password"] if row else None


#CRATING APPOINTMENT
def create_appointment(patient_username: str, doctor_name: str, date: str, time: str, reason: str):
    conn = get_conn()
    cur = conn.cursor()
    #PARAMETERIZED QUERIES
    sql = """
        INSERT INTO appointments (patient_username, doctor_name, date, time, reason)
        VALUES (?, ?, ?, ?, ?)
    """

    cur.execute(sql, (patient_username, doctor_name, date, time, reason))
    conn.commit()
    conn.close()

# UPDATE APPOINTMENT
def update_appointment(apt_id: int, patient_username: str, doctor_name: str, date: str, time: str, reason: str, status: str = "scheduled"):
    conn = get_conn()
    cur = conn.cursor()
    #PARAMETERIZED QUERIES
    sql = """
        UPDATE appointments
        SET patient_username = ?, doctor_name = ?, date = ?, time = ?, reason = ?, created_at = created_at
        WHERE id = ?
    """
    cur.execute(sql, (patient_username, doctor_name, date, time, reason, apt_id))
    conn.commit()
    conn.close()


#DELETE APPOINTMENT
def delete_appointment(apt_id: int):
    conn = get_conn()
    cur = conn.cursor()
    #PARAMETERIZED QUERIES
    cur.execute("DELETE FROM appointments WHERE id = ?", (apt_id,))
    conn.commit()
    conn.close()

def get_appointment() -> List[Dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM appointments ORDER BY date, time")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

#APPOINTMENT ID
def get_appointment_id(apt_id: int):
    conn = get_conn()
    cur = conn.cursor()
    #PARAMETERIZED QUERIES
    cur.execute("SELECT * FROM appointments WHERE id = ?", (apt_id,))
    row = cur.fetchone()

    conn.close()
    return dict(row) if row else None
