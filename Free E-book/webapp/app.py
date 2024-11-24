from flask import Flask, render_template, request, jsonify, send_file
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json

app = Flask(__name__)

# You'll need to set your SendGrid API key in your environment
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
FROM_EMAIL = 'your-verified-sender@yourdomain.com'  # You'll need to verify this email in SendGrid

def send_confirmation_email(to_email):
    try:
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=to_email,
            subject='Your Free E-book Download - The Cycle',
            html_content='''
                <h2>Thank you for your interest in The Cycle!</h2>
                <p>Your free e-book is ready to download. Click the link below:</p>
                <p><a href="http://localhost:8000/download">Download The Cycle</a></p>
                <p>Enjoy your reading!</p>
            ''')
        
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-email', methods=['POST'])
def submit_email():
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Store email in a JSON file
        emails_file = 'subscriber_list.json'
        emails = []
        if os.path.exists(emails_file):
            with open(emails_file, 'r') as f:
                try:
                    emails = json.load(f)
                except:
                    emails = []
        
        # Add new email with timestamp
        from datetime import datetime
        emails.append({
            'email': email,
            'timestamp': datetime.now().isoformat()
        })
        
        # Save updated list
        with open(emails_file, 'w') as f:
            json.dump(emails, f, indent=2)
        
        # Send confirmation email
        if send_confirmation_email(email):
            return jsonify({'message': 'Success! Check your email for the download link.'}), 200
        else:
            return jsonify({'error': 'Error sending confirmation email'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download')
def download():
    try:
        file_path = os.path.join(app.root_path, 'static', 'TheCycle.pdf')
        if not os.path.exists(file_path):
            print(f"File not found at: {file_path}")
            return jsonify({'error': 'File not found'}), 404
        return send_file(file_path, as_attachment=True, download_name='TheCycle.pdf')
    except Exception as e:
        print(f"Download error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
