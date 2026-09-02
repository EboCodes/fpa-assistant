# FPA Assistant - Changelog & Release History
**The Federal Polytechnic, Ado-Ekiti**

All notable updates, architectural changes, and bug fixes for FPA Assistant are documented in this file.

---

## [1.5.0] - 2026-09-02

### Added
- **Expanded Knowledge Base (55 Records)**: Sourced and seeded 27 additional verified entries from `fedpolyado.edu.ng` across all 11 institutional categories (`database/schema/knowledge_base_expanded_seed.sql`).
- **Conversational Intent Classifier**: Added intelligent detection for natural greetings, identity questions, and gratitude statements with immediate polite responses.
- **Multi-Model Gemini Cascade**: Integrated `models/gemini-flash-lite-latest` and `models/gemini-3.7-flash`, achieving sub-second query latency (~0.62s).
- **Smart Direct Fallback**: Replaced raw Q&A dumping with a synthesized direct answer ranking algorithm that responds directly to the student's question.

### Changed
- Increased Gunicorn WSGI timeout to `--timeout 90` in `start-services.sh` to prevent worker timeouts under burst loads.
- Updated system prompt instructions to strictly answer only what the user asks without preamble or data dumps.

---

## [1.4.0] - 2026-09-02

### Added
- **Online Shipping Guide**: Created `docs/ONLINE_DEPLOYMENT_GUIDE.md` detailing deployment to Cloud PaaS (Render/Railway) and Ubuntu Cloud VPS with Nginx and SSL.
- **Admin Email Provisioning**: Initialized and seeded `joshua@ajala.com` with role `admin` in PostgreSQL.

### Changed
- **Rebranded to FPA Assistant**: Updated all branding, browser titles, and headers from generic titles to **FPA Assistant** (*The Federal Polytechnic, Ado-Ekiti*).
- **Eradication of AI Slop**: Removed all cartoon emojis (`🎓`, `🤖`, `💬`, `⚡`, `📌`, `➔`, `👍`, `👎`), neon glow effects, and buzzwords; replaced with an official institutional forest green (`#004D2E`) design system and clean SVG vector icons.
- **Knowledge Base Restricted**: Completely removed the public "Knowledge Base" button and route from student/guest view; access is restricted exclusively to authenticated administrators.

---

## [1.3.0] - 2026-09-02

### Added
- **Unified Production Orchestration**: Created `start-services.sh`, `stop-services.sh`, and `status-services.sh` for lifecycle management.
- **Static SPA Asset Serving**: Node.js Express configured to serve the compiled React bundle from `frontend/dist` with client-side SPA routing fallback.
- **Automated Verification Suite**: Built `backend/src/e2e_verification.js` validating 14 critical paths across backend, database, and AI microservice.

---

## [1.2.0] - 2026-09-02

### Added
- **Rich Markdown Parser**: Custom `FormattedText` parser supporting bold text, bullet points, numbered lists, and hyperlinks.
- **Message Feedback Loop**: Added `POST /api/chat/feedback` endpoint and interactive feedback buttons on message bubbles.
- **Conversation History Drawer**: Sidebar allowing authenticated students to revisit past multi-turn dialogues.
- **Admin Dashboard**: Analytics cards, category/status filters, and full modal form for creating, editing, and deleting knowledge base records.

---

## [1.1.0] - 2026-09-02

### Added
- Seeded initial 24 verified institutional records from `database/schema/knowledge_base_seed.sql`.
- Built `backend/src/seed_admin.js` for administrator initialization and password hashing.
- Added multi-turn conversation context injection into LLM prompts.

---

## [1.0.0] - Initial Prototype
- Basic React frontend prototype.
- Initial Express API structure.
- Python Flask NLP microservice with spaCy.
- Initial PostgreSQL DDL schema (`initial_schema.sql`).
