# model.py
from transformers import pipeline

# Load the pre-trained summarization model (T5 or BART)
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summarizer = pipeline("summarization", model="t5-small")


def generate_summary(text):
    # Summarize text (max tokens set to 1024, adjust as needed)
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

#  Loading Other Functions 













