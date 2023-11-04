from transformers import pipeline
from typing import Any


class SentimentAnalysisFilter:
    sentiment_classifier: Any

    def __init__(self):
        self.sentiment_classifier = pipeline("sentiment-analysis")

    def calculateSentimentScore(self, chat_message: str):
        sentiment_score = self.sentiment_classifier(chat_message)

        return sentiment_score
