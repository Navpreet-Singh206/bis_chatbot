import re


def clean_text(text):
    # Remove markdown links but keep the link text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

    # Remove image tags
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', text)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove navigation garbage
    text = re.sub(r'English\s*/.*?AA\s*', '', text)

    # Remove encoded garbage characters
    text = re.sub(r'[àáâãäåæçèéêëìíîïðñòóôõöøùúûüý]+', '', text)
    text = re.sub(r'Â+', '', text)

    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)

    # Remove excessive special characters
    text = re.sub(r'[\\|•·]+', ' ', text)

    # Keep only readable ASCII and Hindi Unicode
    text = re.sub(r'[^\x20-\x7E\u0900-\u097F]', ' ', text)

    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def is_meaningful(text, min_length=100):
    # Check if text has enough English content to be useful
    if len(text) < min_length:
        return False

    english_chars = sum(1 for c in text if ord(c) < 128 and c.isalpha())
    total_chars = sum(1 for c in text if c.isalpha())

    if total_chars == 0:
        return False

    english_ratio = english_chars / total_chars
    return english_ratio > 0.5