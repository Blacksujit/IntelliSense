# app.py
from flask import Flask, render_template, request, jsonify
from model import generate_summary

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.form.get('text')
    
    if not data:
        return jsonify({"error": "No text provided"}), 400

    # Call the summarization function
    summary = generate_summary(data)
    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)
