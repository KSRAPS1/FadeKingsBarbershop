from flask import Flask, render_template, request
import os

app = Flask(__name__)

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
    with open('bookings.csv', 'a') as f:
        f.write(f"{data['name']},{data['phone']},{data['date']},{data['time']}\n")
    return render_template('confirmation.html', name=data['name'])

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.form
    with open('feedback.csv', 'a') as f:
        f.write(f"{data['name']}, {data['message']}\n")
    return render_template('thank_you.html', name=data['name'])


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)