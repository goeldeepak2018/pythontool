from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
from faker import Faker
import io
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
fake = Faker()


# Email bhejne ka reusable function
def send_notification_email(subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'info@qrinqr.com'
    msg['To'] = 'dummy@safeportpass.com'  # Static target email
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('mail.qrinqr.com', 465) as server:
            server.login('info@qrinqr.com', 'AAPKA_ACTUAL_PASSWORD') 
            server.send_message(msg)
            print("Email sent successfully for row!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Aapka Form Submit Route (Naam apne hisaab se match kar lein, jaise /submit-form)
@app.route('/submit-row', methods=['POST'])
def submit_row():
    # Frontend JS JSON bhej raha hai ya Form data, dono handle ho jayenge
    data = request.json if request.is_json else request.form 
    
    # Email ki body dynamically generate karein
    email_body = "New Row Submitted Details:\n\n"
    for key, value in data.items():
        email_body += f"{key.capitalize()}: {value}\n"
        
    # Trigger Email
    send_notification_email(
        subject="New Row Data from PythonTool",
        body=email_body
    )
    
    return jsonify({"status": "success", "message": "Row processed and email sent!"})



@app.route('/')
def index():
    return render_template('index.html')

# Dummy CSV Download Route (30 rows)
@app.route('/download-dummy', methods=['GET'])


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