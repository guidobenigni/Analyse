from flask import Flask, request, jsonify, render_template
import pdfplumber
import re
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
def upload():
    if 'pdf' not in request.files:
        return jsonify({'error': 'Kein PDF gefunden'}), 400

    file = request.files['pdf']
    
    if file.filename == '':
        return jsonify({'error': 'Keine Datei ausgewählt'}), 400
    
    if file and file.filename.lower().endswith('.pdf'):
        swimmer_details = extract_swimmers(file)
        result = f'Gefundene Schwimmer: {len(swimmer_details)}.\nDetails:\n' + '\n'.join(swimmer_details)
        return jsonify({'result': result})
    else:
        return jsonify({'error': 'Bitte eine gültige PDF-Datei hochladen.'}), 400

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=os.getenv('PORT', 5000))
