# app.py
from flask import Flask, render_template, request, jsonify
import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Try to import the necessary functions from the model
try:
    from ML_Model.model import (
        generate_summary, get_wikipedia_summary, get_stock_info, 
        analyze_sentiment, summarize_url, extract_keywords,
        translate_text, convert_currency, get_readability_score, 
        generate_questions, named_entity_recognition
    )
except ImportError as e:
    print(f"Error: Could not import functions from 'ML_Model.model'. {str(e)}")
    sys.exit(1)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json.get('text')
    if not data or not data.strip():
        return jsonify({"error": "Please enter a value for text"}), 400
    try:
        summary = generate_summary(data)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/summarize_url', methods=['POST'])
def summarize_url_route():
    url = request.json.get('url')
    if not url or not url.strip():
        return jsonify({"error": "Please enter a valid URL"}), 400
    try:
        summary = summarize_url(url)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/wikipedia_summary', methods=['POST'])
def wikipedia_summary():
    topic = request.json.get('topic')
    if not topic or not topic.strip():
        return jsonify({"error": "Please enter a topic"}), 400
    try:
        summary = get_wikipedia_summary(topic)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/stock_info', methods=['POST'])
def stock_info():
    ticker = request.json.get('ticker')
    if not ticker or not ticker.strip():
        return jsonify({"error": "Please enter a valid stock ticker"}), 400
    try:
        info = get_stock_info(ticker)
        return jsonify({"info": info})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/analyze_sentiment', methods=['POST'])
def sentiment():
    text = request.json.get('text')
    if not text or not text.strip():
        return jsonify({"error": "Please enter text for sentiment analysis"}), 400
    try:
        sentiment = analyze_sentiment(text)
        return jsonify({"sentiment": sentiment})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/extract_keywords', methods=['POST'])
def keyword_extraction():
    text = request.json.get('text')
    if not text or not text.strip():
        return jsonify({"error": "Please enter text for keyword extraction"}), 400
    try:
        keywords = extract_keywords(text)
        return jsonify({"keywords": keywords})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/named_entity_recognition', methods=['POST'])
def ner():
    text = request.json.get('text')
    if not text or not text.strip():
        return jsonify({"error": "Please enter text for named entity recognition"}), 400
    try:
        entities = named_entity_recognition(text)
        return jsonify({"entities": entities})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/translate_text', methods=['POST'])
def translate():
    text = request.json.get('text')
    target_language = request.json.get('target_language')
    if not text or not text.strip() or not target_language or not target_language.strip():
        return jsonify({"error": "Please enter text and target language for translation"}), 400
    try:
        translation = translate_text(text, target_language)
        return jsonify({"translation": translation})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/convert_currency', methods=['POST'])
def currency_conversion():
    amount = request.json.get('amount')
    from_currency = request.json.get('from_currency')
    to_currency = request.json.get('to_currency')
    if not amount or not from_currency or not to_currency or not str(amount).strip() or not from_currency.strip() or not to_currency.strip():
        return jsonify({"error": "Please enter valid values for amount, from currency, and to currency"}), 400
    try:
        converted_amount = convert_currency(float(amount), from_currency, to_currency)
        return jsonify({"conversion": converted_amount})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/get_readability_score', methods=['POST'])
def readability():
    text = request.json.get('text')
    if not text or not text.strip():
        return jsonify({"error": "Please enter text for readability scoring"}), 400
    try:
        score = get_readability_score(text)
        return jsonify({"readability_score": score})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/generate_questions', methods=['POST'])
def questions():
    text = request.json.get('text')
    if not text or not text.strip():
        return jsonify({"error": "Please enter text to generate questions"}), 400
    try:
        generated_questions = generate_questions(text)
        return jsonify({"questions": generated_questions})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
