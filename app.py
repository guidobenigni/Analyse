from flask import Flask, request, jsonify
import pdfplumber
import re

app = Flask(__name__)

def extract_swimmers(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    # Regex, um Schwimmer der SV Aqua-Motion Vienna Dolphins und ihre Zeiten zu finden
    swimmers = re.findall(r'(SV Aqua-Motion Vienna Dolphins).+?(\d{4}).+?(\d{2}:\d{2},\d{2})', text)
    
    # Liste mit Schwimmern, Jahrgang und geschwommener Zeit
    swimmer_details = [f"Team: {swimmer[0]}, Jahrgang: {swimmer[1]}, Zeit: {swimmer[2]}" for swimmer in swimmers]

    return swimmer_details

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'Kein PDF gefunden'}), 400

    file = request.files['pdf']
    swimmer_details = extract_swimmers(file)
    result = f'Gefundene Schwimmer: {len(swimmer_details)}.\nDetails:\n' + '\n'.join(swimmer_details)
    
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
