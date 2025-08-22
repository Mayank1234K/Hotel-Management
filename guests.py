# guests.py
from database import get_connection

def register_guest(name, phone, email, address):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO guests (name, phone, email, address) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, phone, email, address))
    conn.commit()
    guest_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return guest_id

def list_guests():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guests")
    guests = cursor.fetchall()
    cursor.close()
    conn.close()
    return guests
