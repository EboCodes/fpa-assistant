# FPA Assistant - The Federal Polytechnic, Ado-Ekiti

**Official AI-Powered Student Information & Administrative Helpdesk**

FPA Assistant is an enterprise-grade conversational AI platform specifically engineered for **The Federal Polytechnic, Ado-Ekiti (Ekiti State, Nigeria)**. It provides students, prospective applicants, and staff with 24/7 verified guidance on admissions, tuition and fee payments, online course registration, examination timetables, MIS results, hostel accommodation, and campus services.

---

## 🎯 System Highlights

- **Institutional Knowledge Base**: Over **55 verified data records** sourced directly from `fedpolyado.edu.ng` across 11 key service categories.
- **Conversational Intelligence**: Powered by Google Gemini (`models/gemini-flash-lite-latest` and `models/gemini-3.7-flash`) with sub-second response times, natural conversational greeting detection, and strict question-focused answers (zero data dumping).
- **Human-Crafted Institutional UI**: Dignified Federal Polytechnic forest green (`#004D2E`) design system, completely free of AI slop, cartoon emojis, or generic marketing buzzwords.
- **Private Knowledge Base**: The knowledge base is strictly reserved for administrative management in the Admin Panel and hidden from the public interface.
- **Student Accounts & Chat History**: Secure user registration, persistent multi-turn conversation memory, and message-level feedback rating (`/api/chat/feedback`).
- **Complete Admin Portal**: Real-time analytics, category filtering, and full Create, Read, Update, and Delete (CRUD) operations on institutional records.

---

## 🏗️ Architecture & Technology Stack

```text
[ Web Browser (Desktop / Mobile) ]
                │
                ▼ (Port 5000)
┌─────────────────────────────────────────────────────────────┐
│ Node.js Express Server                                      │
│ - Serves Compiled Production React SPA (frontend/dist)      │
│ - REST API Authentication (JWT)                             │
│ - Conversation Persistence & Feedback Storage               │
│ - Admin Endpoints & Analytics                               │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼ (:5432)                      ▼ (:5001)
┌─────────────────────────────┐┌──────────────────────────────┐
│ PostgreSQL 14+ Database     ││ Python 3.11 AI Microservice  │
│ - 9 Normalized Tables       ││ - Flask + Gunicorn WSGI      │
│ - 11 Service Categories     ││ - spaCy NLP & NLTK           │
│ - 55 Verified KB Records    ││ - Multi-Model Gemini Cascade │
└─────────────────────────────┘└──────────────┬───────────────┘
                                              │
                                              ▼ (HTTPS / API)
                               ┌──────────────────────────────┐
                               │ Google Gemini API            │
                               │ (gemini-flash-lite-latest)   │
                               └──────────────────────────────┘
```

- **Frontend**: React 18, Vite 5, React Router v6, custom responsive SVG design system.
- **Backend**: Node.js 20+, Express, pg-promise, bcryptjs, jsonwebtoken, helmet, cors.
- **AI Microservice**: Python 3.11, Flask, Gunicorn 21.2, Google Generative AI SDK, spaCy (`en_core_web_sm`), NLTK.
- **Database**: PostgreSQL 14+ on port 5432 (`educational_assistant`).

---

## 🚀 Quick Start & Management

The repository includes unified lifecycle management scripts at the root directory:

### 1. Start All Services
```bash
./start-services.sh
```
*Checks PostgreSQL, compiles frontend assets if missing, launches Gunicorn AI microservice (:5001) and Node.js backend (:5000), and validates live endpoints.*

*(Optional: Add `--dev` to launch the Vite hot-reload development server on port 5173).*

### 2. Check System Health & Metrics
```bash
./status-services.sh
```

### 3. Stop All Services
```bash
./stop-services.sh
```

---

## 🌐 Live URLs & Access

| Resource | URL | Details |
| :--- | :--- | :--- |
| **Web Application** | [http://localhost:5000/](http://localhost:5000/) | Production Single Page Application |
| **REST API Base** | [http://localhost:5000/api](http://localhost:5000/api) | Express API |
| **Admin Portal** | [http://localhost:5000/admin](http://localhost:5000/admin) | Administrative Dashboard |
| **AI Microservice** | [http://localhost:5001/health](http://localhost:5001/health) | Flask / Gunicorn healthcheck |

### 🔑 Administrator Credentials
- **Email**: `joshua@ajala.com`
- **Password**: `Admin123!`

---

## 📁 Repository Directory Structure

```text
Ajala/
├── frontend/                     # React Single-Page Application
│   ├── src/
│   │   ├── App.jsx              # Main UI routing, components, and views
│   │   ├── App.css              # Official institutional design system
│   │   └── main.jsx             # React entry point
│   ├── dist/                    # Compiled production bundle
│   └── package.json
│
├── backend/                      # Node.js + Express REST API
│   ├── src/
│   │   ├── server.js            # Express routes, controllers, and static server
│   │   ├── seed_admin.js        # Administrator creation/promotion utility
│   │   └── e2e_verification.js  # 14-point automated test suite
│   ├── .env                     # Database and JWT configuration
│   └── package.json
│
├── ai-service/                   # Python 3.11 NLP & LLM Microservice
│   ├── src/
│   │   ├── main.py              # Flask microservice entry point
│   │   ├── response_generator.py# Conversational cascade & intelligence engine
│   │   ├── nlp_processor.py     # spaCy text processing
│   │   └── intent_recognizer.py # Query categorization
│   ├── venv/                    # Dedicated Python 3.11 virtual environment
│   ├── .env                     # Gemini API credentials and model configuration
│   └── requirements.txt
│
├── database/                     # PostgreSQL Database Schemas & Seeds
│   └── schema/
│       ├── initial_schema.sql   # DDL for 9 core tables
│       ├── knowledge_base_seed.sql # Initial 24 Q&A records
│       └── knowledge_base_expanded_seed.sql # 27 comprehensive records from fedpolyado.edu.ng
│
├── docs/                         # Detailed Documentation
│   ├── API.md                   # Complete REST API specification
│   ├── ARCHITECTURE.md          # In-depth technical architecture
│   ├── KNOWLEDGE_BASE.md        # Knowledge base taxonomy & management
│   ├── ONLINE_DEPLOYMENT_GUIDE.md # Cloud & VPS shipping instructions
│   ├── SETUP.md                 # Developer installation guide
│   ├── IMPLEMENTATION_SUMMARY.md# Full feature implementation review
│   ├── SYSTEM_VERIFICATION_REPORT.md # Verification records
│   └── CHANGELOG.md             # Detailed release history
│
├── logs/                         # Background runtime logs
├── start-services.sh             # Production service launcher
├── stop-services.sh              # Service shutdown utility
├── status-services.sh            # Live health and metric inspector
├── docker-compose.yml           # Containerized orchestration
└── README.md
```

---

## 📚 Service Categories (55 Active Records)

1. **Admission** (10 records): ND full-time cut-offs, Part-time/evening entry, HND requirements (Lower credit + 1-yr IT, Pass + 2-yr IT), ₦45,000 acceptance fee, academic schools.
2. **School Fees** (7 records): Remita payment procedures, RRR generation, payment verification, resolving pending debits, support contacts.
3. **Course Registration** (6 records): Portal steps, credit unit limits (15 min – 24 max), Add/Drop window, approval signatures.
4. **Examination** (6 records): 75% attendance rule, exam eligibility, carryovers, official NBTE grading scale.
5. **Academic Calendar** (5 records): 15-week semester structure, Rector Engr. Dr. Temitope John Alake, Registry, Bursary.
6. **Hostel Services** (3 records): Abuja Hall of Residence, Student Affairs allocation, prohibited appliances.
7. **SIWES** (3 records): 4-month practical attachment, ITF logbook, assessment & defense.
8. **Library Services** (3 records): Central Library, opening hours, e-library, borrowing rules.
9. **ICT Support** (6 records): Helpdesk phone (07088391544, 09083892022), support emails, password recovery.
10. **Transcript Services** (2 records): Online transcript application, verification, dispatch.
11. **Graduation Requirements** (4 records): Minimum 2.00 CGPA, 6-unit institutional clearance, NYSC mobilization.

---

## 🚢 Shipping Online

Refer to [docs/ONLINE_DEPLOYMENT_GUIDE.md](docs/ONLINE_DEPLOYMENT_GUIDE.md) for full deployment instructions:
- **Cloud PaaS (Render / Railway)**: Deploy managed PostgreSQL, Python AI microservice, and Node.js web app.
- **Ubuntu Cloud VPS (DigitalOcean / AWS / Linode / Campus Server)**: Setup systemd daemons, Nginx reverse proxy, and free Let's Encrypt SSL (`certbot --nginx -d assistant.fedpolyado.edu.ng`).

---

## 🧪 Automated Testing

Run the end-to-end verification suite against all live endpoints:
```bash
node backend/src/e2e_verification.js
```
*(Validates 14 checks: backend health, AI service health, categories, KB search, admin auth, analytics, KB CRUD operations, student registration, authenticated chat, history retrieval, and feedback submission).*

---

## 👤 Project Author

- **AJALA JOSHUA OLUWAFERANMI** (Matric No: `FPA/CS/24/3-0089`)
- **Department**: Computer Science, The Federal Polytechnic, Ado-Ekiti
- **Admin Contact**: `joshua@ajala.com`
