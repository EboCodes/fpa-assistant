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
    """Generate intelligent conversational responses to student inquiries."""

    def __init__(self):
        self.llm_provider = os.getenv("LLM_PROVIDER", "gemini").lower()

        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")

        self.backend_url = os.getenv(
            'BACKEND_URL',
            'https://fpa-backend-s09g.onrender.com'
        ).rstrip('/')

        # Gemini model fallback order
        self.gemini_models = [
            "models/gemini-2.5-flash",
            "models/gemini-3.7-flash",
            "models/gemini-3.6-flash",
            "models/gemini-flash-latest",
            "models/gemini-flash-lite-latest",
        ]

        logger.info(
            "Response Generator initialized (Provider: %s)",
            self.llm_provider
        )

    # ============================================================
    # CONVERSATIONAL RESPONSES
    # ============================================================

    def _check_conversational_greeting(
        self,
        message: str
    ) -> Optional[str]:

        clean = message.strip().lower()
        clean = re.sub(r"[^\w\s]", "", clean)
        clean = re.sub(r"\s+", " ", clean)

        greetings = {
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
            "how are you",
            "howdy",
            "greetings",
            "salut",
        }

        if clean in greetings:
            return (
                "Hello! I am the official FPA Assistant for "
                "The Federal Polytechnic, Ado-Ekiti.\n\n"
                "How can I assist you today? You can ask me about "
                "admissions, school fees and Remita payment, course "
                "registration, examination timetables, hostel "
                "accommodation, or portal support."
            )

        identity_queries = {
            "who are you",
            "what are you",
            "what can you do",
            "what do you do",
            "help me",
            "help",
        }

        if clean in identity_queries:
            return (
                "I am the FPA Assistant, the institutional helpdesk "
                "assistant for The Federal Polytechnic, Ado-Ekiti.\n\n"
                "I can help with admissions, school fees and payments, "
                "course registration, examinations, academic information, "
                "hostel services, portal support, transcripts, and "
                "graduation requirements."
            )

        thanks = {
            "thank you",
            "thanks",
            "thank u",
            "thanks a lot",
            "appreciate it",
        }

        if clean in thanks:
            return (
                "You're very welcome! If you have any other questions "
                "about The Federal Polytechnic, Ado-Ekiti, feel free to ask."
            )

        return None

    # ============================================================
    # KB SUFFICIENCY & SOURCE EXTRACTION HELPERS
    # ============================================================

    def _is_kb_sufficient(
        self,
        kb_entries: List[Dict],
        query: str
    ) -> bool:
        """
        Determine if internal Knowledge Base records contain sufficient,
        high-confidence information to answer the student's query.
        """
        if not kb_entries:
            return False

        query_clean = query.lower().strip()
        query_words = set(
            word for word in re.findall(r"\b[a-zA-Z0-9]+\b", query_clean)
            if len(word) > 2
        )

        if not query_words:
            return False

        stopwords = {
            "the", "and", "is", "are", "was", "were", "where", "what", "how", "who", "when",
            "why", "which", "do", "does", "did", "can", "could", "would", "should", "school",
            "polytechnic", "institution", "federal", "ado", "ekiti", "fpa", "about", "for",
            "with", "from", "that", "this", "have", "has", "had", "get", "tell", "give", "know", "please"
        }

        significant_words = set(w for w in query_words if w not in stopwords)
        if not significant_words:
            significant_words = query_words

        top_entry = kb_entries[0]
        question = str(top_entry.get("question", "")).lower()
        keywords = str(top_entry.get("keywords", "")).lower()
        answer = str(top_entry.get("answer", "")).lower()

        # If exact query string matches question or keywords
        if query_clean in question or query_clean in keywords:
            return True

        # Calculate word match ratio against question and keywords specifically
        matched = 0
        for word in significant_words:
            if word in question or word in keywords:
                matched += 2
            elif word in answer:
                matched += 1

        max_possible = len(significant_words) * 2
        match_ratio = matched / max_possible if max_possible > 0 else 0

        # Require at least 50% match on specific non-stopword intent terms
        return match_ratio >= 0.5

    def _extract_sources_from_gemini_response(
        self,
        response: Any
    ) -> List[Dict[str, str]]:
        """Extract structured web sources from Gemini grounding metadata."""
        sources = []
        if not response:
            return sources

        try:
            candidates = getattr(response, "candidates", []) or []
            if not candidates:
                return sources

            cand = candidates[0]
            gm = getattr(cand, "grounding_metadata", None)
            if not gm:
                return sources

            chunks = getattr(gm, "grounding_chunks", []) or []
            seen_urls = set()

            for chunk in chunks:
                web = getattr(chunk, "web", None)
                if web:
                    uri = str(getattr(web, "uri", "") or "").strip()
                    title = str(getattr(web, "title", "") or "").strip()
                    if uri and uri not in seen_urls:
                        seen_urls.add(uri)
                        if not title:
                            # Clean domain as fallback title
                            title = uri.split("//")[-1].split("/")[0]
                        sources.append({
                            "title": title,
                            "url": uri
                        })
        except Exception as e:
            logger.warning("Error extracting grounding sources: %s", str(e))

        return sources

    # ============================================================
    # MAIN RESPONSE GENERATION
    # ============================================================

    def generate(
        self,
        user_message: str,
        intent: Dict[str, Any],
        context: Dict = None
    ) -> Dict[str, Any]:

        context = context or {}

        query = user_message.strip()

        if not query:
            return {
                "answer": (
                    "Please enter a question and I will help you with "
                    "information about The Federal Polytechnic, Ado-Ekiti."
                ),
                "sources": [],
                "mode": "institutional"
            }

        # Handle greetings, thanks and identity questions first
        conversational_reply = self._check_conversational_greeting(query)

        if conversational_reply:
            return {
                "answer": conversational_reply,
                "sources": [],
                "mode": "institutional"
            }

        # Retrieve relevant institutional knowledge
        kb_entries = self._retrieve_kb_entries(
            query,
            category_id=intent.get("category_id"),
            top_n=6
        )

        is_sufficient = self._is_kb_sufficient(kb_entries, query)

        # Build prompt
        context_text = self._build_context(
            kb_entries if is_sufficient else [],
            query,
            intent,
            context=context,
            use_web_search=not is_sufficient
        )

        # ========================================================
        # GEMINI
        # ========================================================

        if self.llm_provider == "gemini" and self.google_api_key:

            result = self._generate_with_gemini_cascade(
                query,
                context_text,
                intent,
                kb_entries=kb_entries,
                enable_grounding=not is_sufficient
            )

            if result and isinstance(result, dict) and result.get("answer"):
                return result

        # ========================================================
        # OPENAI FALLBACK
        # ========================================================

        if self.llm_provider == "openai" and self.openai_api_key:

            answer = self._generate_with_openai(
                query,
                context_text,
                intent,
                kb_entries=kb_entries
            )

            if answer:
                return {
                    "answer": answer,
                    "sources": [],
                    "mode": "institutional" if is_sufficient else "web_assisted"
                }

        # ========================================================
        # LOCAL FALLBACK
        # ========================================================

        fallback_answer = self._generate_with_template(
            kb_entries,
            intent,
            query=query
        )

        return {
            "answer": fallback_answer,
            "sources": [],
            "mode": "institutional" if is_sufficient else "web_assisted"
        }

    # ============================================================
    # KNOWLEDGE BASE RETRIEVAL
    # ============================================================

    def _retrieve_kb_entries(
        self,
        query: str,
        category_id: int = None,
        top_n: int = 6
    ) -> List[Dict]:

        try:

            entries = []

            # ----------------------------------------------------
            # First attempt: category + search
            # ----------------------------------------------------

            params = {
                "search": query
            }

            if category_id:
                category_name = self._get_category_name(category_id)

                if category_name:
                    params["category"] = category_name

            response = requests.get(
                f"{self.backend_url}/api/kb",
                params=params,
                timeout=8
            )

            if response.status_code == 200:
                data = response.json()
                entries = data.get("data", [])

            # ----------------------------------------------------
            # Second attempt: search without category
            # ----------------------------------------------------

            if not entries:

                response = requests.get(
                    f"{self.backend_url}/api/kb",
                    params={"search": query},
                    timeout=8
                )

                if response.status_code == 200:
                    data = response.json()
                    entries = data.get("data", [])

            # ----------------------------------------------------
            # Third attempt: retrieve entire category
            # ----------------------------------------------------

            if not entries and category_id:

                category_name = self._get_category_name(category_id)

                if category_name:

                    response = requests.get(
                        f"{self.backend_url}/api/kb",
                        params={"category": category_name},
                        timeout=8
                    )

                    if response.status_code == 200:
                        data = response.json()
                        entries = data.get("data", [])

            # ----------------------------------------------------
            # Rank results locally
            # ----------------------------------------------------

            if entries:

                query_words = set(
                    word
                    for word in re.findall(
                        r"\b[a-zA-Z0-9]+\b",
                        query.lower()
                    )
                    if len(word) > 2
                )

                def score_entry(entry):

                    question = str(
                        entry.get("question", "")
                    ).lower()

                    answer = str(
                        entry.get("answer", "")
                    ).lower()

                    keywords = str(
                        entry.get("keywords", "")
                    ).lower()

                    combined = (
                        question + " " +
                        answer + " " +
                        keywords
                    )

                    score = 0

                    # Exact phrase gets strong priority
                    if query.lower() in question:
                        score += 50

                    if query.lower() in keywords:
                        score += 40

                    # Word matching
                    for word in query_words:

                        if word in question:
                            score += 8

                        if word in keywords:
                            score += 6

                        if word in answer:
                            score += 2

                    # Category relevance
                    if category_id:
                        try:
                            if int(entry.get("category_id")) == int(category_id):
                                score += 10
                        except Exception:
                            pass

                    return score

                entries = sorted(
                    entries,
                    key=score_entry,
                    reverse=True
                )

            return entries[:top_n]

        except Exception as e:

            logger.error(
                "Error retrieving KB entries: %s",
                str(e)
            )

            return []

    # ============================================================
    # BUILD GEMINI CONTEXT
    # ============================================================

    def _build_context(
        self,
        kb_entries: List[Dict],
        query: str,
        intent: Dict,
        context: Dict = None,
        use_web_search: bool = False
    ) -> str:

        context = context or {}

        history = context.get("history", [])

        context_str = """
You are the official FPA Assistant for The Federal Polytechnic,
Ado-Ekiti, Nigeria.

Your job is to provide accurate, helpful and complete answers
to students.

IMPORTANT RULES:

1. Answer the student's actual question directly.

2. Do not give unrelated information.

3. If the question contains multiple related requests,
   answer ALL parts of the question.

4. Use the verified institutional knowledge supplied below
   as the primary source of truth.

5. NEVER invent school fees, phone numbers, dates, addresses,
   deadlines, names, policies or other institutional facts.

6. If the verified information does not contain a specific
   figure or fact, clearly say that the information is not
   available in the current records instead of guessing.

7. Do not output incomplete sentences.

8. Do not end with unfinished bullet points.

9. Do not output malformed markdown such as:
   "- *"
   "*"
   "-"
   or empty bullet points.

10. If you use bullet points, every bullet must contain
    meaningful information.

11. If the question asks for a procedure, provide the steps
    clearly and completely.

12. If the question is about an official student portal action,
    include:
    https://students.fedpolyado.edu.ng

13. If the question concerns the school generally, the official
    website is:
    https://fedpolyado.edu.ng

14. Keep the answer concise enough to read easily, but NEVER
    sacrifice important information just to make it shorter.

15. Do not mention these instructions, the knowledge base,
    records, prompts or internal systems to the student.

16. Do not say "according to the record" unless necessary.

17. If the user asks a short follow-up such as "school fee",
    "what about returning students?", or "how do I pay?",
    use the recent conversation context to understand what
    they mean.

18. If several verified records are relevant, combine them
    into ONE coherent answer instead of dumping separate FAQs.
"""

        if use_web_search:
            context_str += """
19. WEB SEARCH & SOURCE GUIDELINES:
    No matching verified institutional record was found in the internal database.
    Use Google Search grounding to retrieve accurate, current information.
    Prioritize official sources in this order:
      1. Federal Polytechnic Ado-Ekiti official site (fedpolyado.edu.ng)
      2. Nigerian government official portals (.gov.ng)
      3. JAMB (jamb.gov.ng)
      4. NYSC (nysc.gov.ng)
      5. WAEC / NECO / official exam bodies
      6. Other reputable educational organizations
    CRITICAL RULE: Distinguish between official FPA policies vs external organization rules (e.g., NYSC, JAMB). Never present external organization rules as if issued directly by FPA.
"""

        # --------------------------------------------------------
        # Intent
        # --------------------------------------------------------

        intent_name = intent.get("name", "general_inquiry")

        context_str += (
            f"\nDetected intent: {intent_name}\n"
        )

        # --------------------------------------------------------
        # Conversation history
        # --------------------------------------------------------

        if history:

            context_str += "\nRecent Conversation:\n"

            for turn in history[-6:]:

                user_msg = str(
                    turn.get("user_message", "")
                ).strip()

                assistant_msg = str(
                    turn.get("ai_response", "")
                ).strip()

                if user_msg:

                    context_str += (
                        f"Student: {user_msg}\n"
                    )

                if assistant_msg:

                    # Keep useful history without making prompt huge
                    if len(assistant_msg) > 500:
                        assistant_msg = assistant_msg[:500] + "..."

                    context_str += (
                        f"FPA Assistant: {assistant_msg}\n"
                    )

        # --------------------------------------------------------
        # Current question
        # --------------------------------------------------------

        context_str += (
            f"\nCurrent Student Question:\n{query}\n"
        )

        # --------------------------------------------------------
        # Verified knowledge
        # --------------------------------------------------------

        if kb_entries:

            context_str += (
                "\nVerified Institutional Information:\n"
            )

            for index, entry in enumerate(
                kb_entries,
                start=1
            ):

                question = str(
                    entry.get("question", "")
                ).strip()

                answer = str(
                    entry.get("answer", "")
                ).strip()

                source = str(
                    entry.get("source", "")
                ).strip()

                context_str += (
                    f"\n[Information {index}]\n"
                    f"Question: {question}\n"
                    f"Answer: {answer}\n"
                )

                if source:
                    context_str += (
                        f"Source: {source}\n"
                    )

        else:

            context_str += """
No directly matching verified institutional record
was found in internal database.
"""

        context_str += """

Now answer the student's current question.

Make sure the final answer is COMPLETE.
If the answer requires several points, include all relevant
points before finishing.
"""

        return context_str

    # ============================================================
    # GEMINI GENERATION
    # ============================================================

    def _generate_with_gemini_cascade(
        self,
        query: str,
        context: str,
        intent: Dict,
        kb_entries: List[Dict] = None,
        enable_grounding: bool = False
    ) -> Optional[Dict[str, Any]]:

        try:

            import google.generativeai as genai

            genai.configure(
                api_key=self.google_api_key
            )

        except Exception as e:

            logger.error(
                "Could not initialize Gemini: %s",
                str(e)
            )

            return None

        preferred = os.getenv(
            "LLM_MODEL",
            "models/gemini-3.6-flash"
        ).strip()

        models_to_try = [preferred]

        for model_name in self.gemini_models:

            if model_name not in models_to_try:
                models_to_try.append(model_name)

        for model_name in models_to_try:

            if not model_name.startswith("models/"):
                model_name = f"models/{model_name}"

            # If grounding requested, try with grounding first, then without tools on error
            tool_modes = ["google_search_retrieval"] if enable_grounding else [None]

            for tool_opt in tool_modes:
                try:

                    logger.info(
                        "Trying Gemini model: %s (grounding: %s)",
                        model_name,
                        bool(tool_opt)
                    )

                    if tool_opt:
                        model = genai.GenerativeModel(
                            model_name=model_name,
                            tools=tool_opt
                        )
                    else:
                        model = genai.GenerativeModel(
                            model_name=model_name
                        )

                    response = model.generate_content(
                        context,
                        generation_config={
                            "temperature": 0.25,
                            "max_output_tokens": 3072,
                        },
                        request_options={
                            "timeout": 35
                        }
                    )

                    if not response:
                        continue

                    text = getattr(
                        response,
                        "text",
                        ""
                    )

                    if not text:
                        continue

                    text = self._clean_response(text)

                    if self._is_complete_response(text):

                        logger.info(
                            "Gemini generated a valid response."
                        )

                        sources = (
                            self._extract_sources_from_gemini_response(response)
                            if tool_opt else []
                        )

                        mode = "web_assisted" if (tool_opt and sources) or enable_grounding else "institutional"

                        return {
                            "answer": text,
                            "sources": sources,
                            "mode": mode
                        }

                    logger.warning(
                        "Gemini returned an incomplete or malformed response "
                        "from %s. Trying next option.",
                        model_name
                    )

                except Exception as e:

                    logger.warning(
                        "Gemini model %s (grounding=%s) failed: %s",
                        model_name,
                        bool(tool_opt),
                        str(e)[:200]
                    )

                    continue

        logger.warning(
            "All Gemini models failed or returned invalid responses. "
            "Using local fallback."
        )

        return None

    # ============================================================
    # OPENAI
    # ============================================================

    def _generate_with_openai(
        self,
        query: str,
        context: str,
        intent: Dict,
        kb_entries: List[Dict] = None
    ) -> Optional[str]:

        try:

            from openai import OpenAI

            client = OpenAI(
                api_key=self.openai_api_key,
                timeout=15.0
            )

            response = client.chat.completions.create(
                model=os.getenv(
                    "LLM_MODEL",
                    "gpt-3.5-turbo"
                ),
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are the official FPA Assistant "
                            "for The Federal Polytechnic, Ado-Ekiti. "
                            "Give accurate, complete and concise answers."
                        )
                    },
                    {
                        "role": "user",
                        "content": context
                    }
                ],
                temperature=0.25,
                max_tokens=800
            )

            text = (
                response.choices[0]
                .message
                .content
                or ""
            ).strip()

            text = self._clean_response(text)

            if self._is_complete_response(text):
                return text

        except Exception as e:

            logger.warning(
                "OpenAI request failed: %s",
                str(e)
            )

        return self._generate_with_template(
            kb_entries or [],
            intent,
            query=query
        )

    # ============================================================
    # RESPONSE CLEANING
    # ============================================================

    def _clean_response(self, text: str) -> str:

        if not text:
            return ""

        text = text.strip()

        # Remove accidental code fences around plain answers
        text = re.sub(
            r"^```(?:markdown|text)?\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"\s*```$",
            "",
            text
        )

        # Remove empty bullet lines
        lines = []

        for line in text.splitlines():

            stripped = line.strip()

            if stripped in {
                "-",
                "*",
                "•",
                "- *",
                "* -",
                "- **",
                "* **",
            }:
                continue

            lines.append(line.rstrip())

        text = "\n".join(lines).strip()

        # Remove repeated blank lines
        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )

        return text

    # ============================================================
    # CHECK WHETHER RESPONSE IS COMPLETE
    # ============================================================

    def _is_complete_response(self, text: str) -> bool:

        if not text:
            return False

        clean = text.strip()

        # Too short to be a useful institutional response
        if len(clean) < 20:
            return False

        # Check for unclosed markdown links cut off mid-url e.g. "[https" or "[text]("
        if re.search(r"\[https?:\/\/[^\s\]]*$", clean) or re.search(r"\[[^\]]{1,100}$", clean):
            return False

        # Obvious malformed endings or trailing prepositions from truncation
        bad_endings = (
            "-",
            "*",
            "•",
            ":",
            "**",
            "```",
        )

        if clean.endswith(bad_endings):
            return False

        words = clean.split()
        if words:
            last_word = words[-1].lower()
            if last_word in {"at", "the", "and", "or", "to", "of", "in", "for", "with"}:
                return False

        # Detect incomplete numbered list item at the end e.g. "1." or "2. "
        if re.search(r"\n\d+\.\s*$", clean):
            return False

        # Detect empty bullet lines
        for line in clean.splitlines():

            stripped = line.strip()

            if stripped in {
                "-",
                "*",
                "•",
                "- *",
                "* -",
            }:
                return False

        # Must contain at least one alphanumeric character
        if not re.search(r"[A-Za-z0-9]", clean):
            return False

        return True

    # ============================================================
    # LOCAL KNOWLEDGE-BASE FALLBACK
    # ============================================================

    def _generate_with_template(
        self,
        kb_entries: List[Dict],
        intent: Dict,
        query: str = ""
    ) -> str:

        if not kb_entries:

            return (
                "I could not find a verified answer to that question "
                "in my current institutional information.\n\n"
                "Please check the official Federal Polytechnic, "
                "Ado-Ekiti website at **https://fedpolyado.edu.ng** "
                "or use the student portal at "
                "**https://students.fedpolyado.edu.ng**."
            )

        # --------------------------------------------------------
        # Rank records
        # --------------------------------------------------------

        query_words = set(
            word
            for word in re.findall(
                r"\b[a-zA-Z0-9]+\b",
                query.lower()
            )
            if len(word) > 2
        )

        def score_entry(entry):

            question = str(
                entry.get("question", "")
            ).lower()

            answer = str(
                entry.get("answer", "")
            ).lower()

            keywords = str(
                entry.get("keywords", "")
            ).lower()

            score = 0

            if query.lower() in question:
                score += 50

            if query.lower() in keywords:
                score += 40

            for word in query_words:

                if word in question:
                    score += 8

                if word in keywords:
                    score += 6

                if word in answer:
                    score += 2

            return score

        ranked = sorted(
            kb_entries,
            key=score_entry,
            reverse=True
        )

        best = ranked[0]

        answer = str(
            best.get("answer", "")
        ).strip()

        source = str(
            best.get("source", "")
        ).strip()

        if not answer:

            return (
                "I found an institutional record related to your "
                "question, but it does not contain a complete answer.\n\n"
                "Please verify the latest information through "
                "**https://fedpolyado.edu.ng**."
            )

        answer = self._clean_response(answer)

        # --------------------------------------------------------
        # Add source only when useful
        # --------------------------------------------------------

        response = answer

        if source:

            response += (
                f"\n\n*Source: {source}*"
            )

        # --------------------------------------------------------
        # Portal link for relevant student services
        # --------------------------------------------------------

        service_intents = {
            "admission",
            "course_registration",
            "fees",
            "examination",
            "academic_calendar",
            "hostel",
            "siwes",
            "library",
            "ict_support",
            "transcript",
            "graduation",
        }

        if intent.get("name") in service_intents:

            response += (
                "\n\nFor student portal services, visit "
                "**https://students.fedpolyado.edu.ng**."
            )

        return response

    # ============================================================
    # CATEGORY MAPPING
    # ============================================================

    def _get_category_name(
        self,
        category_id: int
    ) -> Optional[str]:

        mapping = {
            1: "Admission",
            2: "Course Registration",
            3: "School Fees",
            4: "Examination",
            5: "Academic Calendar",
            6: "Hostel Services",
            7: "SIWES",
            8: "Library Services",
            9: "ICT Support",
            10: "Transcript Services",
            11: "Graduation Requirements",
        }

        return mapping.get(category_id)