# ai-service/src/response_generator.py
"""
Response Generation module
Generates conversational, intelligent, and context-focused responses
for The Federal Polytechnic, Ado-Ekiti (FPA Assistant).
"""

import os
import re
import logging
from typing import Dict, List, Any, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class ResponseGenerator:
    """Generate intelligent conversational responses to student inquiries"""
    
    def __init__(self):
        """Initialize response generator"""
        self.llm_provider = os.getenv('LLM_PROVIDER', 'gemini').lower()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.backend_url = os.getenv('BACKEND_URL', 'http://localhost:5000')
        
        # Priority list of Gemini models for fast, intelligent responses
        self.gemini_models = [
            'models/gemini-flash-lite-latest',
            'models/gemini-3.7-flash',
            'models/gemini-3.6-flash',
            'models/gemini-flash-latest'
        ]
        
        logger.info(f"✅ Response Generator initialized (Provider: {self.llm_provider})")

    def _check_conversational_greeting(self, message: str) -> Optional[str]:
        """Detect natural greetings or conversational intents and reply directly."""
        clean = message.strip().lower()
        clean = re.sub(r'[^\w\s]', '', clean)
        
        greetings = {'hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'how are you', 'howdy', 'greetings', 'salut'}
        if clean in greetings or any(clean.startswith(g + ' ') for g in ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return (
                "Hello! I am the official FPA Assistant for The Federal Polytechnic, Ado-Ekiti. "
                "How can I assist you today? You can ask me about admissions, school fees and Remita payment, "
                "course registration, examination timetables, hostel accommodation, or portal support."
            )
            
        identity_queries = {'who are you', 'what are you', 'what can you do', 'what do you do', 'help me', 'help'}
        if clean in identity_queries:
            return (
                "I am the FPA Assistant, the official institutional helpdesk service for The Federal Polytechnic, Ado-Ekiti. "
                "I provide verified information regarding admissions, fee payments, semester registrations, examinations, "
                "MIS results, and student affairs."
            )
            
        thanks = {'thank you', 'thanks', 'thank u', 'thanks a lot', 'appreciate it'}
        if clean in thanks:
            return (
                "You are very welcome! If you have any further questions regarding The Federal Polytechnic, Ado-Ekiti, "
                "feel free to ask anytime. Have a productive academic session!"
            )
            
        return None
    
    def generate(self, user_message: str, intent: Dict[str, Any], context: Dict = None) -> str:
        """
        Generate response to user message with conversational intelligence.
        """
        context = context or {}
        user_message_clean = user_message.strip()

        # Step 1: Check for natural conversational statements (greetings/thanks)
        greeting_reply = self._check_conversational_greeting(user_message_clean)
        if greeting_reply:
            return greeting_reply

        # Step 2: Retrieve relevant KB entries
        kb_entries = self._retrieve_kb_entries(
            user_message_clean,
            category_id=intent.get('category_id')
        )
        
        # Step 3: Build context for LLM including conversation history
        context_text = self._build_context(kb_entries, user_message_clean, intent, context=context)
        
        # Step 4: Generate response using LLM cascade or template
        if self.llm_provider == 'gemini' and self.google_api_key:
            response = self._generate_with_gemini_cascade(user_message_clean, context_text, intent, kb_entries=kb_entries)
        elif self.openai_api_key and self.llm_provider == 'openai':
            response = self._generate_with_openai(user_message_clean, context_text, intent, kb_entries=kb_entries)
        else:
            response = self._generate_with_template(kb_entries, intent, query=user_message_clean)
        
        return response
    
    def _retrieve_kb_entries(self, query: str, category_id: int = None, top_n: int = 4) -> List[Dict]:
        """Retrieve relevant KB entries matching the query"""
        try:
            params = {'search': query}
            if category_id:
                cat_name = self._get_category_name(category_id)
                if cat_name:
                    params['category'] = cat_name
            
            response = requests.get(
                f"{self.backend_url}/api/kb",
                params=params,
                timeout=5
            )
            
            entries = []
            if response.status_code == 200:
                entries = response.json().get('data', [])
            
            # If search filter returned empty, fetch general category entries
            if not entries and category_id:
                cat_name = self._get_category_name(category_id)
                if cat_name:
                    res_cat = requests.get(
                        f"{self.backend_url}/api/kb",
                        params={'category': cat_name},
                        timeout=5
                    )
                    if res_cat.status_code == 200:
                        entries = res_cat.json().get('data', [])
            
            return entries[:top_n]
            
        except Exception as e:
            logger.error(f"Error retrieving KB entries: {str(e)}")
            return []
    
    def _build_context(self, kb_entries: List[Dict], query: str, intent: Dict, context: Dict = None) -> str:
        """Build a strict, focused context string for the LLM."""
        context = context or {}
        history = context.get('history', [])

        context_str = """System Identity: You are the official FPA Assistant for The Federal Polytechnic, Ado-Ekiti.
Your task is to answer the student's question conversationally, politely, and intelligently.

CRITICAL INSTRUCTIONS:
1. Answer ONLY the specific question asked by the user. Do not provide unrelated FAQ lists or dump raw data.
2. Be concise, direct, and conversational. Use clean markdown formatting (bullet points, bold text for key figures).
3. If the answer involves official actions, include the direct portal link (https://students.fedpolyado.edu.ng) or main website (https://fedpolyado.edu.ng).
4. Maintain context from recent conversation turns when resolving follow-up questions or pronouns.
5. If verified institutional information is provided below, prioritize it strictly.
"""
        if history:
            context_str += "\nRecent Conversation History:\n"
            for turn in history[-4:]:
                u_msg = turn.get('user_message', '').strip()
                a_msg = turn.get('ai_response', '').strip()
                if u_msg:
                    context_str += f"Student: {u_msg}\n"
                if a_msg:
                    # Truncate long past responses to preserve prompt focus
                    context_str += f"FPA Assistant: {a_msg[:160]}...\n"

        context_str += f"\nCurrent Student Inquiry: \"{query}\"\n"

        if kb_entries:
            context_str += "\nVerified Institutional Knowledge:\n"
            for i, entry in enumerate(kb_entries, 1):
                context_str += f"[Record {i}]\nQuestion: {entry.get('question', '')}\nAnswer: {entry.get('answer', '')}\nSource: {entry.get('source', 'Institutional Notice')}\n\n"

        return context_str
    
    def _generate_with_gemini_cascade(self, query: str, context: str, intent: Dict, kb_entries: List[Dict] = None) -> str:
        """Try fast Gemini models in sequence with timeout guards."""
        import google.generativeai as genai

        genai.configure(api_key=self.google_api_key)

        preferred = os.getenv('LLM_MODEL', 'models/gemini-flash-lite-latest').strip()
        models_to_try = [preferred] + [m for m in self.gemini_models if m != preferred]

        for model_name in models_to_try:
            if not model_name.startswith('models/'):
                model_name = f"models/{model_name}"

            try:
                model = genai.GenerativeModel(model_name=model_name)
                
                response = model.generate_content(
                    context,
                    generation_config={
                        'temperature': 0.4,
                        'max_output_tokens': 600,
                    },
                    request_options={'timeout': 10}
                )

                if response and response.text:
                    return response.text.strip()

            except Exception as e:
                logger.warning(f"Gemini model {model_name} failed: {str(e)[:100]}. Trying next fallback...")
                continue

        # If all Gemini models fail or quota is exhausted, use smart synthesized template fallback
        logger.warning("All Gemini candidate models failed; executing intelligent fallback.")
        return self._generate_with_template(kb_entries or [], intent, query=query)

    def _generate_with_openai(self, query: str, context: str, intent: Dict, kb_entries: List[Dict] = None) -> str:
        """Generate response using OpenAI API."""
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.openai_api_key, timeout=12.0)
            response = client.chat.completions.create(
                model=os.getenv('LLM_MODEL', 'gpt-3.5-turbo'),
                messages=[
                    {
                        "role": "system",
                        "content": "You are the official assistant for The Federal Polytechnic, Ado-Ekiti. Answer only what the student asks, directly and conversationally."
                    },
                    {
                        "role": "user",
                        "content": context
                    }
                ],
                temperature=0.4,
                max_tokens=500
            )
            
            return (response.choices[0].message.content or '').strip()
            
        except Exception as e:
            logger.warning(f"OpenAI API request failed: {str(e)}; executing fallback.")
            return self._generate_with_template(kb_entries or [], intent, query=query)
    
    def _generate_with_template(self, kb_entries: List[Dict], intent: Dict, query: str = "") -> str:
        """
        Intelligent conversational fallback:
        Ranks retrieved entries to find the single most relevant answer to the user's specific request.
        Does NOT dump multiple Q&A entries.
        """
        if not kb_entries:
            return (
                "Regarding your inquiry, specific institutional details were not found in our current records. "
                "Please verify directly via the official Federal Polytechnic, Ado-Ekiti student portal at "
                "**https://students.fedpolyado.edu.ng** or contact the Directorate of Academic Affairs."
            )
        
        # Rank entries by word overlap with the user's query
        query_words = set(re.findall(r'\w+', query.lower()))
        
        def score_entry(entry):
            q_text = entry.get('question', '').lower()
            k_text = entry.get('keywords', '').lower()
            score = 0
            for w in query_words:
                if len(w) > 2:
                    if w in q_text:
                        score += 3
                    if w in k_text:
                        score += 2
            return score

        best_entry = max(kb_entries, key=score_entry)
        answer = best_entry.get('answer', '').strip()
        source = best_entry.get('source', '')

        response = f"{answer}\n\n"
        if source:
            response += f"*Source: {source}*\n"
        response += "For portal services and registration updates, visit **https://students.fedpolyado.edu.ng**."
        
        return response
    
    def _get_category_name(self, category_id: int) -> Optional[str]:
        """Convert category_id to category name string"""
        mapping = {
            1: 'Admission',
            2: 'Course Registration',
            3: 'School Fees',
            4: 'Examination',
            5: 'Academic Calendar',
            6: 'Hostel Services',
            7: 'SIWES',
            8: 'Library Services',
            9: 'ICT Support',
            10: 'Transcript Services',
            11: 'Graduation Requirements'
        }
        return mapping.get(category_id)
