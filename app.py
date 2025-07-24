from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL configuration for XAMPP
db_config = {
    'host': 'localhost',
    'user': 'root',        
    'password': '',        
    'database': 'ticket_booking'
}

# Function to get DB connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        event = request.form['event']
        seats = request.form['seats']

        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO bookings (name, email, event, seats) VALUES (%s, %s, %s, %s)"
        values = (name, email, event, seats)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('index'))
    
    return render_template('booking.html')

@app.route('/bookings')
def bookings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('bookings.html', bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True)
