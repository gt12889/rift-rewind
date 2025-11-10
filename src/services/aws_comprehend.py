"""
AWS Comprehend integration for sentiment analysis and key phrase extraction.
"""
import boto3
from typing import Dict, List
from botocore.exceptions import ClientError
from config.settings import settings


class ComprehendService:
    """Service for AWS Comprehend text analysis."""
    
    def __init__(self):
        self.client = boto3.client(
            'comprehend',
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key
        )
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of text."""
        try:
            response = self.client.detect_sentiment(
                Text=text,
                LanguageCode='en'
            )
            return {
                "sentiment": response['Sentiment'],
                "scores": response['SentimentScore']
            }
        except ClientError as e:
            print(f"Error analyzing sentiment: {e}")
            return {"sentiment": "NEUTRAL", "scores": {}}
    
    def extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases from text."""
        try:
            response = self.client.detect_key_phrases(
                Text=text,
                LanguageCode='en'
            )
            return [phrase['Text'] for phrase in response['KeyPhrases']]
        except ClientError as e:
            print(f"Error extracting key phrases: {e}")
            return []
    
    def analyze_match_commentary(self, match_analysis: str) -> Dict:
        """Analyze match commentary for insights."""
        sentiment = self.analyze_sentiment(match_analysis)
        key_phrases = self.extract_key_phrases(match_analysis)
        
        return {
            "sentiment": sentiment,
            "key_phrases": key_phrases,
            "insights": {
                "tone": sentiment["sentiment"],
                "focus_areas": key_phrases[:5]
            }
        }

