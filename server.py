''' from flask import Flask, request, jsonify
from flask_cors import CORS
from email_classifier import EmailClassifier

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8501"}})

classifier = EmailClassifier()

@app.route('/api/process_emails', methods=['POST'])
def process_emails():
    data = request.get_json()
    try:
        result = classifier.process_emails(
            data['email'],
            data['password'],
            data['imap']
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)'''