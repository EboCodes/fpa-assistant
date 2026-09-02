# FPA Assistant - Complete Setup & Developer Guide
**The Federal Polytechnic, Ado-Ekiti**

This guide outlines the local development setup, environment configuration, database seeding, and service orchestration for FPA Assistant.

---

## 📋 System Prerequisites

- **Operating System**: Linux (Ubuntu 20.04+, Debian, Fedora, Arch) or macOS. (Windows supported via WSL2).
- **Node.js**: Version 18.x or 20.x+ with `npm`.
- **Python**: Version 3.11+ with `pip` and `venv`.
- **PostgreSQL**: Version 14+ (active service on port 5432).
- **Google Gemini API Key**: Free tier or paid API key from Google AI Studio.

---

## 🗄️ Database Setup & Seeding

### 1. Create the Database & User
Log in to PostgreSQL as an administrator:
```bash
sudo -u postgres psql
```

Create the database and assign privileges:
```sql
CREATE DATABASE educational_assistant;
CREATE USER postgres WITH PASSWORD 'ayoade2004';
GRANT ALL PRIVILEGES ON DATABASE educational_assistant TO postgres;
\q
```

### 2. Apply Initial Schema (9 Tables)
```bash
PGPASSWORD=ayoade2004 psql -h localhost -U postgres -d educational_assistant -f database/schema/initial_schema.sql
```

### 3. Seed Verified Institutional Knowledge Base (55 Records)
```bash
# Apply initial institutional records
PGPASSWORD=ayoade2004 psql -h localhost -U postgres -d educational_assistant -f database/schema/knowledge_base_seed.sql

# Apply comprehensive expanded records from fedpolyado.edu.ng
PGPASSWORD=ayoade2004 psql -h localhost -U postgres -d educational_assistant -f database/schema/knowledge_base_expanded_seed.sql
```

---

## 🔧 Component Configuration

### 1. Backend Service Configuration
Create or inspect `backend/.env`:
```env
PORT=5000
NODE_ENV=production
DATABASE_URL=postgresql://postgres:ayoade2004@localhost:5432/educational_assistant
JWT_SECRET=super_secret_jwt_key_fedpolyado_2026_change_in_production
AI_SERVICE_URL=http://localhost:5001
CORS_ORIGIN=*

# Admin Account Email
ADMIN_EMAIL=joshua@ajala.com
```

Install backend dependencies:
```bash
cd backend
npm install
```

Initialize/seed the administrator account (`joshua@ajala.com`):
```bash
node src/seed_admin.js
```
*Expected output: `✅ Admin user created successfully (ID: 5, Email: joshua@ajala.com)`*

### 2. Python AI Microservice Configuration
Create or inspect `ai-service/.env`:
```env
PORT=5001
AI_SERVICE_PORT=5001
BACKEND_URL=http://localhost:5000
LLM_PROVIDER=gemini
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
LLM_MODEL=models/gemini-flash-lite-latest
TEMPERATURE=0.4
```

Create virtual environment and install dependencies:
```bash
cd ai-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
deactivate
```

### 3. Frontend Client Configuration
Install frontend dependencies and generate the production bundle:
```bash
cd frontend
npm install
npm run build
```
*This compiles the React application into `frontend/dist`, which the Node.js backend serves directly on port 5000.*

---

## 🚀 Running the Services

### Standard Production Mode (Recommended)
From the project root:
```bash
./start-services.sh
```

This script:
1. Verifies PostgreSQL connectivity.
2. Checks that `frontend/dist` is compiled.
3. Launches the Python microservice on port 5001 via Gunicorn WSGI (`--timeout 90`).
4. Launches the Node.js backend on port 5000.
5. Runs health validation checks and reports system status.

### Hot-Reload Development Mode
To develop frontend React components with Vite's hot module replacement:
```bash
./start-services.sh --dev
```
- Access the Vite development server at: `http://localhost:5173`
- Access the API and production server at: `http://localhost:5000`

### Checking Live Service Status
```bash
./status-services.sh
```

### Stopping All Services
```bash
./stop-services.sh
```

---

## 🧪 Running Automated Tests

Run the full end-to-end verification suite against the live system:
```bash
node backend/src/e2e_verification.js
```

This verifies:
1. Backend `/health` endpoint
2. AI microservice `:5001/health` endpoint
3. Category retrieval (11 categories)
4. Knowledge base query operations
5. Admin authentication (`joshua@ajala.com`)
6. Admin live analytics metrics
7. Knowledge base Create, Update, and Delete operations
8. Student account registration
9. Multi-turn chat persistence
10. Conversation history drawer retrieval
11. Feedback rating submission (`/api/chat/feedback`)
12. Unified static SPA serving on `/`
