# ai-service/src/intent_recognizer.py

"""
Intent Recognition module
Identifies user intent from messages to route to appropriate KB sections.
"""

import logging
import re
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class IntentRecognizer:
    """Recognize user intent from processed text."""

    def __init__(self):

        self.intent_patterns = {

            # ----------------------------------------------------
            # LOCATION
            # ----------------------------------------------------

            "school_location": {
                "keywords": [
                    "where is the school",
                    "where is fedpoly",
                    "where is federal polytechnic ado ekiti",
                    "school located",
                    "school location",
                    "campus location",
                    "school address",
                    "where is the campus",
                    "location of the school",
                    "address of the school",
                    "where can i find the school",
                ],
                "category_id": None,
                "description":
                    "Questions about the school location and campus address",
            },

            # ----------------------------------------------------
            # ADMISSION
            # ----------------------------------------------------

            "admission": {
                "keywords": [
                    "admission",
                    "apply",
                    "application",
                    "admission requirements",
                    "entrance",
                    "enrollment",
                    "admission form",
                    "application form",
                    "how to apply",
                    "when is admission",
                ],
                "category_id": 1,
                "description":
                    "Questions about admission process and requirements",
            },

            # ----------------------------------------------------
            # COURSE REGISTRATION
            # ----------------------------------------------------

            "course_registration": {
                "keywords": [
                    "course registration",
                    "course register",
                    "register course",
                    "register courses",
                    "register my courses",
                    "registration",
                    "registration process",
                    "registration deadline",
                    "course registration deadline",
                    "add course",
                    "add a course",
                    "drop course",
                    "drop a course",
                    "course form",
                    "registration form",
                ],
                "category_id": 2,
                "description":
                    "Questions about course registration",
            },

            # ----------------------------------------------------
            # SCHOOL FEES
            # ----------------------------------------------------

            "fees": {
                "keywords": [
                    "fees",
                    "fee",
                    "school fee",
                    "school fees",
                    "tuition",
                    "tuition fee",
                    "cost",
                    "payment",
                    "pay fees",
                    "pay school fees",
                    "fee schedule",
                    "school fee schedule",
                    "invoice",
                    "generate invoice",
                    "remita",
                    "remita payment",
                    "payment status",
                    "fee payment",
                    "school charges",
                ],
                "category_id": 3,
                "description":
                    "Questions about school fees and payments",
            },

            # ----------------------------------------------------
            # EXAMINATION
            # ----------------------------------------------------

            "examination": {
                "keywords": [
                    "examination",
                    "exam",
                    "exams",
                    "exam schedule",
                    "exam date",
                    "exam venue",
                    "exam timetable",
                    "examination timetable",
                    "test",
                    "exam result",
                    "examination result",
                ],
                "category_id": 4,
                "description":
                    "Questions about examinations",
            },

            # ----------------------------------------------------
            # ACADEMIC CALENDAR
            # ----------------------------------------------------

            "academic_calendar": {
                "keywords": [
                    "academic calendar",
                    "calendar",
                    "academic year",
                    "semester",
                    "semester start",
                    "semester date",
                    "school calendar",
                    "holiday",
                    "break",
                    "resumption",
                    "resumption date",
                ],
                "category_id": 5,
                "description":
                    "Questions about academic calendar and dates",
            },

            # ----------------------------------------------------
            # HOSTEL
            # ----------------------------------------------------

            "hostel": {
                "keywords": [
                    "hostel",
                    "hostels",
                    "accommodation",
                    "student accommodation",
                    "residence",
                    "living",
                    "hostel application",
                    "hostel fee",
                    "hostel fees",
                    "room",
                    "bed space",
                ],
                "category_id": 6,
                "description":
                    "Questions about hostel services and accommodation",
            },

            # ----------------------------------------------------
            # SIWES
            # ----------------------------------------------------

            "siwes": {
                "keywords": [
                    "siwes",
                    "industrial work",
                    "industrial training",
                    "placement",
                    "work experience",
                    "attachment",
                    "industrial experience",
                    "siwes placement",
                ],
                "category_id": 7,
                "description":
                    "Questions about SIWES",
            },

            # ----------------------------------------------------
            # LIBRARY
            # ----------------------------------------------------

            "library": {
                "keywords": [
                    "library",
                    "library service",
                    "library services",
                    "library card",
                    "borrowing",
                    "borrow book",
                    "reading room",
                    "books",
                ],
                "category_id": 8,
                "description":
                    "Questions about library services",
            },

            # ----------------------------------------------------
            # ICT SUPPORT
            # ----------------------------------------------------

            "ict_support": {
                "keywords": [
                    "portal",
                    "student portal",
                    "portal login",
                    "login",
                    "log in",
                    "technical support",
                    "technical issue",
                    "ict",
                    "password",
                    "forgot password",
                    "account",
                    "website",
                    "portal problem",
                    "portal issue",
                    "cannot login",
                    "can't login",
                ],
                "category_id": 9,
                "description":
                    "Questions about ICT support and portal issues",
            },

            # ----------------------------------------------------
            # TRANSCRIPT
            # ----------------------------------------------------

            "transcript": {
                "keywords": [
                    "transcript",
                    "transcript request",
                    "academic record",
                    "result sheet",
                    "transcript fee",
                    "request transcript",
                ],
                "category_id": 10,
                "description":
                    "Questions about transcript services",
            },

            # ----------------------------------------------------
            # GRADUATION
            # ----------------------------------------------------

            "graduation": {
                "keywords": [
                    "graduation",
                    "graduate",
                    "clearance",
                    "graduation requirement",
                    "graduation requirements",
                    "final year",
                    "convocation",
                    "convocation gown",
                    "gown",
                ],
                "category_id": 11,
                "description":
                    "Questions about graduation requirements",
            },
        }

        logger.info(
            "Intent Recognizer initialized"
        )

    # ============================================================
    # RECOGNIZE INTENT
    # ============================================================

    def recognize(
        self,
        processed_text: str,
        top_n: int = 3
    ) -> Dict[str, Any]:

        text = processed_text.lower().strip()

        # Normalize spaces
        text = re.sub(r"\s+", " ", text)

        # --------------------------------------------------------
        # Empty input
        # --------------------------------------------------------

        if not text:

            return {
                "name": "general_inquiry",
                "confidence": 0.5,
                "category_id": None,
                "description": "General inquiry",
                "suggestions": [],
            }

        # --------------------------------------------------------
        # Strong location detection
        # --------------------------------------------------------

        location_patterns = [
            r"\bwhere\s+is\s+(the\s+)?school\b",
            r"\bwhere\s+is\s+(the\s+)?school\s+located\b",
            r"\bwhere\s+is\s+(the\s+)?school\s+located\s+at\b",
            r"\bwhere\s+is\s+fedpoly\b",
            r"\bwhere\s+is\s+federal\s+polytechnic\b",
            r"\bschool\s+location\b",
            r"\bcampus\s+location\b",
            r"\bschool\s+address\b",
            r"\baddress\s+of\s+(the\s+)?school\b",
            r"\bwhere\s+can\s+i\s+find\s+(the\s+)?school\b",
        ]

        if any(
            re.search(pattern, text)
            for pattern in location_patterns
        ):

            return {
                "name": "school_location",
                "confidence": 0.98,
                "category_id": None,
                "description":
                    "Questions about the school location and campus address",
                "suggestions": [],
            }

        # --------------------------------------------------------
        # Strong course registration detection
        # --------------------------------------------------------
        #
        # This MUST happen before generic admission detection.
        #

        course_registration_patterns = [
            r"\bregister\s+course\b",
            r"\bregister\s+courses\b",
            r"\bregister\s+my\s+courses\b",
            r"\bregistration\b",
            r"\bcourse\s+registration\b",
            r"\bregistration\s+form\b",
            r"\badd\s+(a\s+)?course\b",
            r"\bdrop\s+(a\s+)?course\b",
            r"\bregistration\s+deadline\b",
        ]

        if any(
            re.search(pattern, text)
            for pattern in course_registration_patterns
        ):

            return {
                "name": "course_registration",
                "confidence": 0.96,
                "category_id": 2,
                "description":
                    "Questions about course registration",
                "suggestions": [],
            }

        # --------------------------------------------------------
        # Strong school-fee detection
        # --------------------------------------------------------

        fee_patterns = [
            r"\bschool\s+fee\b",
            r"\bschool\s+fees\b",
            r"\btuition\b",
            r"\bfee\s+schedule\b",
            r"\bfee\s+payment\b",
            r"\bpay\s+(my\s+)?school\s+fees\b",
            r"\bhow\s+much\s+(is|are)\s+(the\s+)?school\s+fees?\b",
            r"\bhow\s+much\s+is\s+(the\s+)?school\s+fee\b",
            r"\bremita\b",
            r"\bgenerate\s+(a\s+)?invoice\b",
        ]

        if any(
            re.search(pattern, text)
            for pattern in fee_patterns
        ):

            return {
                "name": "fees",
                "confidence": 0.96,
                "category_id": 3,
                "description":
                    "Questions about school fees and payments",
                "suggestions": [],
            }

        # --------------------------------------------------------
        # General scoring
        # --------------------------------------------------------

        scores = {}

        for intent_name, intent_data in self.intent_patterns.items():

            score = self._calculate_score(
                text,
                intent_data["keywords"]
            )

            scores[intent_name] = {
                "score": score,
                "data": intent_data,
            }

        sorted_intents = sorted(
            scores.items(),
            key=lambda item: item[1]["score"],
            reverse=True
        )

        # --------------------------------------------------------
        # Primary intent
        # --------------------------------------------------------

        if (
            sorted_intents
            and sorted_intents[0][1]["score"] > 0
        ):

            primary_name, primary_info = sorted_intents[0]

            score = primary_info["score"]

            # More realistic confidence
            confidence = min(
                0.99,
                max(
                    0.5,
                    score / 100
                )
            )

            primary_intent = {
                "name": primary_name,
                "confidence": confidence,
                "category_id":
                    primary_info["data"]["category_id"],
                "description":
                    primary_info["data"]["description"],
            }

        else:

            primary_intent = {
                "name": "general_inquiry",
                "confidence": 0.5,
                "category_id": None,
                "description": "General inquiry",
            }

        # --------------------------------------------------------
        # Suggestions
        # --------------------------------------------------------

        suggestions = []

        for intent_name, intent_info in sorted_intents:

            if intent_name == primary_intent["name"]:
                continue

            if intent_info["score"] <= 0:
                continue

            suggestions.append({
                "name": intent_name,
                "confidence": min(
                    0.99,
                    max(
                        0.25,
                        intent_info["score"] / 100
                    )
                ),
                "category_id":
                    intent_info["data"]["category_id"],
            })

            if len(suggestions) >= top_n - 1:
                break

        primary_intent["suggestions"] = suggestions

        return primary_intent

    # ============================================================
    # SCORE INTENT
    # ============================================================

    def _calculate_score(
        self,
        text: str,
        keywords: List[str]
    ) -> float:

        score = 0

        for keyword in keywords:

            keyword = keyword.lower().strip()

            if not keyword:
                continue

            # Exact phrase
            if re.search(
                rf"\b{re.escape(keyword)}\b",
                text
            ):

                # Longer phrases are stronger signals
                word_count = len(
                    keyword.split()
                )

                if word_count >= 3:
                    score += 30
                elif word_count == 2:
                    score += 20
                else:
                    score += 8

                continue

            # Partial multi-word matching
            keyword_words = keyword.split()

            if len(keyword_words) > 1:

                matched_words = sum(
                    1
                    for word in keyword_words
                    if re.search(
                        rf"\b{re.escape(word)}\b",
                        text
                    )
                )

                required = max(
                    2,
                    len(keyword_words) - 1
                )

                if matched_words >= required:

                    score += (
                        matched_words * 5
                    )

        return score

    # ============================================================
    # GET CATEGORY INTENT
    # ============================================================

    def get_category_intent(
        self,
        category_id: int
    ) -> Dict[str, Any]:

        for intent_name, intent_data in self.intent_patterns.items():

            if intent_data["category_id"] == category_id:

                return {
                    "name": intent_name,
                    "category_id": category_id,
                    "keywords": intent_data["keywords"],
                    "description":
                        intent_data["description"],
                }

        return None

    # ============================================================
    # GET ALL INTENTS
    # ============================================================

    def get_all_intents(
        self
    ) -> List[Dict[str, Any]]:

        intents = []

        for intent_name, intent_data in self.intent_patterns.items():

            intents.append({
                "name": intent_name,
                "category_id":
                    intent_data["category_id"],
                "description":
                    intent_data["description"],
                "keywords":
                    intent_data["keywords"],
            })

        return intents