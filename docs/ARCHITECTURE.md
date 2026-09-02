# FPA Assistant - Technical System Architecture
**The Federal Polytechnic, Ado-Ekiti**

---

## 🏗️ High-Level Architectural Diagram

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│                         CLIENT TIER (React SPA)                          │
│                                                                           │
│  ┌───────────────────────┐  ┌────────────────────┐  ┌─────────────────┐ │
│  │ Student Helpdesk      │  │ Overview Directory │  │ Admin Panel     │ │
│  │ - Natural Dialogue    │  │ - 6 Major Areas    │  │ - Metrics Cards │ │
│  │ - History Drawer      │  │ - Quick Inquiries  │  │ - KB CRUD Modal │ │
│  │ - Feedback System     │  │ - Institutional    │  │ - Filter Bar    │ │
│  └───────────────────────┘  └────────────────────┘  └─────────────────┘ │
│                                                                           │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     │ HTTPS / HTTP (Port 5000)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│                  APPLICATION & API TIER (Node.js + Express)             │
│                                Port 5000                                 │
│                                                                           │
│  - Static Asset Delivery: Serves compiled React bundle (frontend/dist)  │
│  - Authentication & Authorization: JWT issuing and verification         │
│  - REST Controllers: /api/auth, /api/chat, /api/admin, /api/kb          │
│  - Conversation Management: Persistence & session tracking              │
│  - Connection Pool: pg-promise with automatic transaction management    │
│                                                                           │
└─────────────────┬───────────────────────────────────────┬───────────────┘
                  │                                       │
      PostgreSQL  │ (Port 5432)               HTTP (JSON) │ (Port 5001)
                  ▼                                       ▼
┌──────────────────────────────────┐    ┌──────────────────────────────────┐
│        DATABASE TIER             │    │       AI MICROSERVICE TIER       │
│      PostgreSQL 14+              │    │      Python 3.11 + Gunicorn      │
│                                  │    │            Port 5001             │
│ - users (students & admins)      │    │                                  │
│ - categories (11 services)       │    │ - Greeting & Intent Classifier   │
│ - knowledge_base (55 records)    │    │ - spaCy NLP Pipeline             │
│ - conversations & chat_messages  │    │ - Knowledge Retrieval            │
│ - feedback & analytics           │    │ - Gemini Cascade LLM Generator   │
└──────────────────────────────────┘    └────────────────┬─────────────────┘
                                                         │
                                                         │ HTTPS API
                                                         ▼
                                        ┌──────────────────────────────────┐
                                        │        GOOGLE GEMINI API         │
                                        │ - gemini-flash-lite-latest       │
                                        │ - gemini-3.7-flash               │
                                        └──────────────────────────────────┘
```

---

## 🔄 End-to-End Query Lifecycle

```text
[1. Student Inputs Inquiry]
          │
          ▼
[2. Express: POST /api/chat/message]
          │
          ├── Authenticate JWT (if logged in) or assign guest session
          ├── Retrieve past 4 message turns from chat_messages
          ▼
[3. AI Microservice: POST /api/process]
          │
          ├── A. Conversational Greeting Check
          │      └─ If greeting ("hello", "who are you"): Return direct greeting immediately
          │
          ├── B. Intent Recognition & Category Matching
          │      └─ Sift message through spaCy NLP pipeline
          │
          ├── C. Knowledge Base Retrieval
          │      └─ Query Backend: GET /api/kb?category=...&search=...
          │
          ├── D. Prompt Synthesis
          │      └─ Assemble System Persona + Multi-Turn History + Verified KB Records
          │
          └── E. Multi-Model LLM Execution
                 ├─ Attempt 1: models/gemini-flash-lite-latest (timeout: 10s)
                 ├─ Attempt 2: models/gemini-3.7-flash (timeout: 10s)
                 └─ Fallback: Synthesized direct answer from best-matching KB record
          │
          ▼
[4. Express Records Transaction]
          │
          ├── Persist user query and AI response into chat_messages
          ├── Generate unique messageId
          ▼
[5. Client Receives Response]
          │
          ├── Formatted Markdown rendering (clean lists, bold text, links)
          └── Interactive Feedback widget triggers POST /api/chat/feedback
```

---

## 📦 Database Entity-Relationship Model

The PostgreSQL database (`educational_assistant`) comprises 9 normalized tables:

1. **`categories`**: Defines the 11 institutional domains (Admission, Course Registration, School Fees, Examination, Academic Calendar, Hostel Services, SIWES, Library Services, ICT Support, Transcript Services, Graduation Requirements).
2. **`users`**: Stores student and administrator accounts with bcrypt-hashed passwords and role attributes (`student`, `admin`).
3. **`knowledge_base`**: Stores 55 verified Q&A records with category foreign keys, full-text keywords, source attribution, and active status indicators.
4. **`embeddings`**: Reserved for vector representations of knowledge base entries for local cosine similarity search.
5. **`conversations`**: Maintains distinct chat sessions linked to student user IDs.
6. **`chat_messages`**: Captures each interaction turn (`user_message`, `ai_response`, `intent`, `confidence`, and timestamps).
7. **`feedback`**: Captures student evaluation ratings (1–5 scale) and feedback comments linked to specific `message_id` records.
8. **`analytics`**: Logs aggregated interaction counts and query frequencies.
9. **`admin_logs`**: Audit trail of administrative modifications to knowledge base entries.

---

## 🛡️ Security & Performance Architecture

- **Stateless Authentication**: Signed JSON Web Tokens (JWT) using HMAC-SHA256 with 7-day expiration.
- **Data Protection**: Sensitive passwords hashed via bcrypt (10 salt rounds).
- **HTTP Security**: Helmet middleware with secure headers, CORS origin restrictions, and parameterized PostgreSQL queries via pg-promise to prevent SQL injection.
- **Process Supervision**: Gunicorn WSGI multi-worker daemon with configurable timeouts (`--timeout 90`) and automatic crash recovery.
- **Fail-Safe Fallback**: Zero downtime guaranteed by multi-model Gemini fallbacks coupled with local deterministic knowledge base extraction.
