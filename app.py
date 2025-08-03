from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os

DATA_FOLDER = 'data'
os.makedirs(DATA_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'secret4567'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/book')
def book_page():
    return render_template('book.html')


@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    # Save booking to CSV
    with open(os.path.join(DATA_FOLDER, 'bookings.csv'), 'a', newline='') as f:
        f.write(f"{data['name']},{data['phone']},{data['service']},{data['date']},{data['time']}\n")
    return render_template('confirmation.html', name=data['name'])

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.form
    with open(os.path.join(DATA_FOLDER, 'feedback.csv'), 'a', newline='') as f:
        f.write(f"{data['name']}, {data['email']}, {data['message']}\n")
    return render_template('thank_you.html', name=data['name'])

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password4567':
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            return "Incorrect credentials", 401
    return render_template('login.html')

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    bookings = []
    feedback = []

    try:
        with open(os.path.join(DATA_FOLDER, 'bookings.csv'), newline='') as f:
            reader = csv.reader(f)
            bookings = list(reader)
    except FileNotFoundError:
        pass

    try:
        with open(os.path.join(DATA_FOLDER, 'feedback.csv'), newline='') as f:
            reader = csv.reader(f)
            feedback = list(reader)
    except FileNotFoundError:
        pass
    
    return render_template('admin.html', bookings=bookings, feedback=feedback)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route('/delete_booking', methods=['POST'])
def delete_booking():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    index = int(request.form['index'])
    bookings = []

    with open(os.path.join(DATA_FOLDER, 'bookings.csv'), newline='') as f:
        reader = csv.reader(f)
        bookings = list(reader)

    if 0 <= index < len(bookings):
        bookings.pop(index)

    with open(os.path.join(DATA_FOLDER, 'bookings.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(bookings)

    return redirect(url_for('admin'))

@app.route('/delete_feedback', methods=['POST'])
def delete_feedback():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    index = int(request.form['index'])
    feedback = []

    with open(os.path.join(DATA_FOLDER, 'feedback.csv'), newline='') as f:
        reader = csv.reader(f)
        feedback = list(reader)

    if 0 <= index < len(feedback):
        feedback.pop(index)

    with open(os.path.join(DATA_FOLDER, 'feedback.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(feedback)

    return redirect(url_for('admin'))

@app.route('/reply_feedback', methods=['POST'])
def reply_feedback():
    email = request.form['email']
    reply = request.form['reply']
    # Here you would send the reply using an email service or log it
    print(f"Reply sent to {email}: {reply}")
    return redirect(url_for('admin'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)