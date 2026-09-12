from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
from faker import Faker
import io
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
fake = Faker()

@app.route('/')
def index():
    return render_template('index.html')

# Dummy CSV Download Route (30 rows)
@app.route('/download-dummy', methods=['GET'])

def send_email(receiver_email, subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'info@qrinqr.com'
    msg['To'] = receiver_email
    msg.set_content(body)

    # PORT 465 ke liye SMTP_SSL use karna zaroori hai
    try:
        with smtplib.SMTP_SSL('mail.qrinqr.com', 465) as server:
            # Apna actual email password yahan daalein
            server.login('info@qrinqr.com', 'AAPKA_EMAIL_PASSWORD') 
            server.send_message(msg)
            print("Email successfully sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")

        
def download_dummy():
    data = []
    mobiles = ["9412825702", "9811400087"]
    
    for _ in range(30):
        data.append({
            "Name": fake.name(),
            "Email": "dummy@safeportpass.com",
            "Mobile": fake.random_element(elements=mobiles),
            "Subject": fake.sentence(nb_words=3),
            "Comment": fake.text(max_nb_chars=50)
        })
    
    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False)
    output = io.BytesIO(csv_data.encode('utf-8'))
    
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='dummy_contacts.csv'
    )

# CSV Upload & Processing Route
@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    df = pd.read_csv(file)
    # CSV ke data ko dictionary mein convert karke frontend par bhejna
    records = df.to_dict(orient='records')
    
    return jsonify({
        'status': 'success',
        'total': len(records),
        'records': records
    })

if __name__ == '__main__':
    # host='0.0.0.0' zaroori hai taaki Docker ke bahar browser mein access ho sake
    app.run(host='0.0.0.0', port=5000, debug=True)