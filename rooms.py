# rooms.py
from database import get_connection

def add_room(room_number, room_type, status='Available'):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO rooms (room_number, room_type, status) VALUES (%s, %s, %s)"
    cursor.execute(sql, (room_number, room_type, status))
    conn.commit()
    room_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return room_id

def list_rooms():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()
    cursor.close()
    conn.close()
    return rooms

def update_room_status(room_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE rooms SET status=%s WHERE room_id=%s"
    cursor.execute(sql, (status, room_id))
    conn.commit()
    cursor.close()
    conn.close()
