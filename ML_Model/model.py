# model.py
from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize
import torch
import requests
from bs4 import BeautifulSoup
import re
import wikipedia
import yfinance as yf
from textblob import TextBlob
import spacy
from googletrans import Translator
from forex_python.converter import CurrencyRates

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Load spaCy model for named entity recognition
nlp = spacy.load("en_core_web_sm")

# Check if CUDA is available and set the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the pre-trained summarization model (T5)
summarizer = pipeline("summarization", model="t5-small", device=device)

# Initialize translator
translator = Translator()

def preprocess_text(text):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Join sentences back together, limiting to 1024 tokens
    preprocessed_text = " ".join(sentences)
    return preprocessed_text[:1024]

def generate_summary(text):
    try:
        # Preprocess the input text
        preprocessed_text = preprocess_text(text)
        
        # Generate summary
        # Adjusted max_length to be shorter than input length
        input_length = len(preprocessed_text.split())
        max_length = min(input_length - 1, 150)  # Ensure max_length is less than input_length
        summary = summarizer(preprocessed_text, max_length=max_length, min_length=min(50, max_length), do_sample=False)
        
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def scrape_article(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the main content (this may need to be adjusted based on the website structure)
        article = soup.find('article') or soup.find('div', class_='content')
        
        if article:
            # Remove script and style elements
            for script in article(["script", "style"]):
                script.decompose()
            
            # Get text and remove extra whitespace
            text = re.sub(r'\s+', ' ', article.get_text()).strip()
            return text
        else:
            return "Could not extract article content."
    except Exception as e:
        return f"Error scraping article: {str(e)}"

def summarize_url(url):
    article_text = scrape_article(url)
    return generate_summary(article_text)

def get_wikipedia_summary(topic):
    try:
        wiki_summary = wikipedia.summary(topic, sentences=5)
        return generate_summary(wiki_summary)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found. Please be more specific. Options: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{topic}'"
    except Exception as e:
        return f"Error fetching Wikipedia summary: {str(e)}"

def get_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        summary = f"Company: {info.get('longName', 'N/A')}\n"
        summary += f"Current Price: ${info.get('currentPrice', 'N/A'):.2f}\n"
        summary += f"52 Week High: ${info.get('fiftyTwoWeekHigh', 'N/A'):.2f}\n"
        summary += f"52 Week Low: ${info.get('fiftyTwoWeekLow', 'N/A'):.2f}\n"
        summary += f"Market Cap: ${info.get('marketCap', 'N/A'):,}\n"
        summary += f"Description: {generate_summary(info.get('longBusinessSummary', 'N/A'))}"
        return summary
    except Exception as e:
        return f"Error fetching stock information: {str(e)}"

def analyze_sentiment(text):
    try:
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        if sentiment > 0.05:
            return "Positive"
        elif sentiment < -0.05:
            return "Negative"
        else:
            return "Neutral"
    except Exception as e:
        return f"Error analyzing sentiment: {str(e)}"

def extract_keywords(text):
    try:
        # Simple frequency-based approach for keyword extraction
        words = text.lower().split()
        word_freq = {}
        stopwords = set(nltk.corpus.stopwords.words('english'))
        for word in words:
            if word not in stopwords:
                word_freq[word] = word_freq.get(word, 0) + 1
        return sorted(word_freq, key=word_freq.get, reverse=True)[:5]
    except Exception as e:
        return f"Error extracting keywords: {str(e)}"

def translate_text(text, target_language='en'):
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        return f"Error in translation: {str(e)}"

def convert_currency(amount, from_currency, to_currency):
    try:
        c = CurrencyRates()
        return c.convert(from_currency, to_currency, amount)
    except Exception as e:
        return f"Error converting currency: {str(e)}"

def get_readability_score(text):
    try:
        return TextBlob(text).sentiment.subjectivity
    except Exception as e:
        return f"Error calculating readability score: {str(e)}"

def generate_questions(text):
    try:
        doc = nlp(text)
        questions = []
        for sent in doc.sents:
            if len(sent) > 5:  # Only consider sentences with more than 5 words
                subject = [token for token in sent if token.dep_ == "nsubj"]
                if subject:
                    question = f"What does {subject[0]} do in this context?"
                    questions.append(question)
        return questions[:3]  # Return top 3 questions
    except Exception as e:
        return f"Error generating questions: {str(e)}"

def named_entity_recognition(text):
    try:
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
    except Exception as e:
        return f"Error in named entity recognition: {str(e)}"