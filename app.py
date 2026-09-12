from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
from faker import Faker
import io
import smtplib
from email.message import EmailMessage
import urllib.parse
import random
import requests

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
            server.login('info@qrinqr.com', 'ODod@1234$#') 
            server.send_message(msg)
            print("Email sent successfully for row!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Aapka Form Submit Route (Naam apne hisaab se match kar lein, jaise /submit-form)
@app.route('/submit-row', methods=['POST'])
def submit_row():
    data = request.json
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



# 1. Naya SMS Tool Page Route
@app.route('/sms-tool')
def sms_tool():
    return render_template('sms.html')

# 2. 10 Numbers ki Dummy CSV Download karne ka Route
@app.route('/download-sms-dummy')
def download_sms_dummy():
    # Gaurav aur Deepak ke numbers ke sath 10 rows ka data
    data = [
        {"Name": "Gaurav", "Mobile": "9811400087"},
        {"Name": "Deepak", "Mobile": "9412825702"},
        {"Name": "Gaurav", "Mobile": "9811400087"},
        {"Name": "Deepak", "Mobile": "9412825702"},
        {"Name": "Gaurav", "Mobile": "9811400087"},
        {"Name": "Deepak", "Mobile": "9412825702"},
        {"Name": "Gaurav", "Mobile": "9811400087"},
        {"Name": "Deepak", "Mobile": "9412825702"},
        {"Name": "Gaurav", "Mobile": "9811400087"},
        {"Name": "Deepak", "Mobile": "9412825702"},
        {"Name": "Gaurav", "Mobile": "9811400087"},
        {"Name": "Deepak", "Mobile": "9412825702"},
        {"Name": "Gaurav", "Mobile": "9811400087"},
        {"Name": "Deepak", "Mobile": "9412825702"},
    ]
    
    # Baaki 8 rows dummy numbers se bharne ke liye
    #for i in range(3, 11):
    #data.append({"Name": f"User {i}", "Mobile": f"99999999{i:02d}"})
        
    df_sms = pd.DataFrame(data)
    csv_data = df_sms.to_csv(index=False)
    output = io.BytesIO(csv_data.encode('utf-8'))
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='sms_dummy_10.csv')

# 3. SMS Bhejne ka logic (Aapki PHP API ke hisaab se)
@app.route('/send-sms', methods=['POST'])
def send_sms():
    data = request.json if request.is_json else request.form
    mobile = data.get('Mobile', '')

    if not mobile:
        return jsonify({"status": "error", "message": "Mobile number missing"})

    # OTP generate karna (6-digit random number)
    otp = str(random.randint(100000, 999999))
    
    # Message banakar URL Encode karna (PHP ke urlencode() ki tarah)
    msg = f"Your US OTP is :: {otp}  का उपयोग करने के लिए धन्यवाद. Regards, Certisafe."
    encoded_msg = urllib.parse.quote(msg)
    
    # PHP wali same API URL
    url = f"http://smsapi.24x7sms.com/api_2.0/SendUnicodeSMS.aspx?APIKEY=CU3IvoEQ8CU&MobileNo={mobile}&SenderID=VRSAFE&Message={encoded_msg}&ServiceName=TEMPLATE_BASED&DLTTemplateID=1007917856946451195"
    
    try:
        # GET request call (PHP curl ki jagah)
        response = requests.get(url)
        print(f"API Response for {mobile}: {response.text}")
        return jsonify({"status": "success", "message": f"SMS sent to {mobile}"})
    except Exception as e:
        print(f"SMS Error: {e}")
        return jsonify({"status": "error", "message": str(e)})

    
if __name__ == '__main__':
    # host='0.0.0.0' zaroori hai taaki Docker ke bahar browser mein access ho sake
    app.run(host='0.0.0.0', port=5000, debug=True)