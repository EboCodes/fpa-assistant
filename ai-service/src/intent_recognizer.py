# ai-service/src/intent_recognizer.py
"""
Intent Recognition module
Identifies user intent from messages to route to appropriate KB sections
"""

import logging
import re
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class IntentRecognizer:
    """Recognize user intent from processed text"""
    
    def __init__(self):
        """Initialize intent patterns and categories"""
        
        # Define intent patterns and associated categories
        self.intent_patterns = {
            'school_location': {
                'keywords': ['where is the school', 'where is fedpoly', 'where is federal polytechnic adoe ekiti', 'school located', 'campus location', 'school address', 'where is the campus', 'location of the school'],
                'category_id': None,
                'description': 'Questions about the school location and campus address'
            },
            'admission': {
                'keywords': ['admission', 'apply', 'admission requirements', 'entrance', 'enrollment', 'register', 'admission form'],
                'category_id': 1,
                'description': 'Questions about admission process and requirements'
            },
            'course_registration': {
                'keywords': ['course registration', 'register course', 'register courses', 'add course', 'drop course', 'registration deadline'],
                'category_id': 2,
                'description': 'Questions about course registration'
            },
            'fees': {
                'keywords': ['fees', 'tuition', 'cost', 'payment', 'pay fees', 'fee schedule', 'invoice', 'school fee'],
                'category_id': 3,
                'description': 'Questions about school fees and payments'
            },
            'examination': {
                'keywords': ['examination', 'exam', 'exam schedule', 'test', 'exam date', 'exam venue', 'examination timetable', 'exam result'],
                'category_id': 4,
                'description': 'Questions about examinations'
            },
            'academic_calendar': {
                'keywords': ['academic calendar', 'calendar', 'schedule', 'academic year', 'semester', 'holiday', 'break', 'semester start'],
                'category_id': 5,
                'description': 'Questions about academic calendar and dates'
            },
            'hostel': {
                'keywords': ['hostel', 'accommodation', 'residence', 'living', 'hostel application', 'room', 'bed space'],
                'category_id': 6,
                'description': 'Questions about hostel services and accommodation'
            },
            'siwes': {
                'keywords': ['siwes', 'industrial work', 'placement', 'work experience', 'attachment', 'industrial experience'],
                'category_id': 7,
                'description': 'Questions about SIWES (Students Industrial Work Experience Scheme)'
            },
            'library': {
                'keywords': ['library', 'book', 'library service', 'borrowing', 'library card', 'reading room'],
                'category_id': 8,
                'description': 'Questions about library services'
            },
            'ict_support': {
                'keywords': ['portal', 'login', 'ict', 'technical support', 'password', 'account', 'student portal', 'website'],
                'category_id': 9,
                'description': 'Questions about ICT support and portal issues'
            },
            'transcript': {
                'keywords': ['transcript', 'transcript request', 'academic record', 'certificate', 'result sheet', 'transcript fee'],
                'category_id': 10,
                'description': 'Questions about transcript services'
            },
            'graduation': {
                'keywords': ['graduation', 'graduate', 'clearance', 'graduation requirement', 'final year', 'convocation', 'gown'],
                'category_id': 11,
                'description': 'Questions about graduation requirements'
            }
        }
        
        logger.info("✅ Intent Recognizer initialized")
    
    def recognize(self, processed_text: str, top_n: int = 3) -> Dict[str, Any]:
        """
        Recognize intent from processed text
        
        Args:
            processed_text: Cleaned and lemmatized text
            top_n: Number of top intent suggestions to return
        
        Returns:
            Dict with primary intent and suggestions
        """
        text = processed_text.lower()

        if re.search(r'\b(where|what)\s+(is|are)\s+(the\s+)?school\s+(located|located at|address|campus)\b|\b(school\s+located|campus\s+location|school\s+address)\b', text):
            return {
                'name': 'school_location',
                'confidence': 0.96,
                'category_id': None,
                'description': 'Questions about the school location and campus address',
                'suggestions': []
            }

        scores = {}
        for intent_name, intent_data in self.intent_patterns.items():
            score = self._calculate_score(text, intent_data['keywords'])
            scores[intent_name] = {
                'score': score,
                'data': intent_data
            }

        sorted_intents = sorted(
            scores.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )

        if sorted_intents and sorted_intents[0][1]['score'] > 0:
            primary_intent_name, primary_intent_info = sorted_intents[0]
            primary_intent = {
                'name': primary_intent_name,
                'confidence': min(primary_intent_info['score'] / 100, 1.0),
                'category_id': primary_intent_info['data']['category_id'],
                'description': primary_intent_info['data']['description']
            }
        else:
            primary_intent = {
                'name': 'general_inquiry',
                'confidence': 0.5,
                'category_id': None,
                'description': 'General inquiry'
            }

        suggestions = []
        for intent_name, intent_info in sorted_intents[1:top_n]:
            if intent_info['score'] > 0:
                suggestions.append({
                    'name': intent_name,
                    'confidence': min(intent_info['score'] / 100, 1.0),
                    'category_id': intent_info['data']['category_id']
                })

        primary_intent['suggestions'] = suggestions
        return primary_intent
    
    def _calculate_score(self, text: str, keywords: List[str]) -> float:
        """
        Calculate intent score based on keyword matches.
        This avoids low-quality false positives from generic words such as "school".
        """
        score = 0

        for keyword in keywords:
            keyword_pattern = re.escape(keyword)
            if re.search(rf'\b{keyword_pattern}\b', text):
                score += 25
                continue

            keyword_words = keyword.split()
            if len(keyword_words) > 1:
                matched_words = sum(1 for word in keyword_words if re.search(rf'\b{re.escape(word)}\b', text))
                if matched_words >= max(2, len(keyword_words) - 1):
                    score += matched_words * 6
            else:
                if re.search(rf'\b{re.escape(keyword_words[0])}\b', text):
                    score += 5

        return score
    
    def get_category_intent(self, category_id: int) -> Dict[str, Any]:
        """
        Get intent information for a specific category
        
        Args:
            category_id: ID of the category
        
        Returns:
            Intent information for the category
        """
        for intent_name, intent_data in self.intent_patterns.items():
            if intent_data['category_id'] == category_id:
                return {
                    'name': intent_name,
                    'category_id': category_id,
                    'keywords': intent_data['keywords'],
                    'description': intent_data['description']
                }
        
        return None
    
    def get_all_intents(self) -> List[Dict[str, Any]]:
        """
        Get all defined intents
        
        Returns:
            List of all intent definitions
        """
        intents = []
        for intent_name, intent_data in self.intent_patterns.items():
            intents.append({
                'name': intent_name,
                'category_id': intent_data['category_id'],
                'description': intent_data['description'],
                'keywords': intent_data['keywords']
            })
        return intents
