# bookings.py
from database import get_connection
from rooms import update_room_status

def book_room(guest_id, room_id, check_in, check_out):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO bookings (guest_id, room_id, check_in, check_out) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (guest_id, room_id, check_in, check_out))
    conn.commit()
    booking_id = cursor.lastrowid
    # Update room status
    update_room_status(room_id, 'Booked')
    cursor.close()
    conn.close()
    return booking_id

def list_bookings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT b.booking_id, g.name, r.room_number, b.check_in, b.check_out
                      FROM bookings b
                      JOIN guests g ON b.guest_id = g.guest_id
                      JOIN rooms r ON b.room_id = r.room_id""")
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return bookings
