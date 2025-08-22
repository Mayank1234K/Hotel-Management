from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from database import get_connection
import guests
import rooms
import bookings

app = Flask(__name__)
app.secret_key = 'your_strong_secret_key_here'  # Use a strong key in production


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'employee_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT employee_id, password FROM employees WHERE username=%s", (username,))
        employee = cursor.fetchone()
        cursor.close()
        conn.close()

        if employee and employee[1]== password:
            session['employee_id'] = employee  # Store only employee_id, not entire tuple
            session['username'] = username
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash( 'success')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/guests', methods=['GET', 'POST'])
@login_required
def guests_route():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        guests.register_guest(name, phone, email, address)
        flash(f'Guest "{name}" registered successfully.', 'success')
        return redirect(url_for('guests_route'))
    all_guests = guests.list_guests()
    return render_template('guests.html', guests=all_guests)


@app.route('/delete_guest/<int:guest_id>', methods=['POST'])
@login_required
def delete_guest(guest_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM guests WHERE guest_id=%s", (guest_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash(f'Guest ID {guest_id} deleted.', 'success')
    return redirect(url_for('guests_route'))


@app.route('/rooms', methods=['GET', 'POST'])
@login_required
def rooms_route():
    if request.method == 'POST':
        room_number = request.form['room_number']
        room_type = request.form['room_type']
        rooms.add_room(room_number, room_type)
        flash(f'Room "{room_number}" added successfully.', 'success')
        return redirect(url_for('rooms_route'))
    all_rooms = rooms.list_rooms()
    return render_template('rooms.html', rooms=all_rooms)


@app.route('/delete_room/<int:room_id>', methods=['POST'])
@login_required
def delete_room(room_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rooms WHERE room_id=%s", (room_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash(f'Room ID {room_id} deleted.', 'success')
    return redirect(url_for('rooms_route'))


@app.route('/bookings', methods=['GET', 'POST'])
@login_required
def bookings_route():
    if request.method == 'POST':
        guest_id = int(request.form['guest_id'])
        room_id = int(request.form['room_id'])
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        bookings.book_room(guest_id, room_id, check_in, check_out)
        flash('Booking created successfully.', 'success')
        return redirect(url_for('bookings_route'))
    all_bookings = bookings.list_bookings()
    return render_template('bookings.html', bookings=all_bookings)


@app.route('/delete_booking/<int:booking_id>', methods=['POST'])
@login_required
def delete_booking(booking_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE booking_id=%s", (booking_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash(f'Booking ID {booking_id} deleted.', 'success')
    return redirect(url_for('bookings_route'))


if __name__ == '__main__':
    app.run(debug=True)
