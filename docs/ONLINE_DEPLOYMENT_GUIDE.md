# FPA Assistant - Online Deployment & Shipping Guide
**The Federal Polytechnic, Ado-Ekiti**

This guide provides step-by-step instructions to deploy **FPA Assistant** live on the public internet.

---

## Architecture Overview

```text
[ Students & Staff ] 
         │ (HTTPS / 443)
         ▼
    [ Nginx / Cloud PaaS ]
         │
         ├──► [ Frontend + Backend API ] (Node.js on :5000)
         │           │
         │           ├──► [ PostgreSQL Database ] (:5432)
         │           │
         │           └──► [ Python AI Microservice ] (:5001)
         │                       │
         │                       └──► [ Google Gemini API ]
```

- **Unified Web & API App**: Port 5000 (Node.js Express serves the built React SPA and `/api/*` endpoints).
- **AI Microservice**: Port 5001 (Python 3.11 Gunicorn WSGI running NLP & Gemini 3.6 Flash).
- **Database**: PostgreSQL 14+ with 9 tables and verified seed records.

---

## Option 1: Deploy to Cloud PaaS (Render / Railway) - Recommended

This is the easiest path with zero server maintenance, automatic HTTPS, and automated GitHub deployments.

### 1. Push Your Code to GitHub
```bash
cd /home/francis/Downloads/Ajala
git init
git add .
git commit -m "feat: production-ready FPA Assistant"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/fpa-assistant.git
git push -u origin main
```

### 2. Provision a PostgreSQL Database on Render or Railway
- Create a new PostgreSQL instance.
- Copy the **Internal Database URL** (e.g., `postgresql://postgres:...@.../dbname`).
- Run the schema and seed scripts against the database:
  ```bash
  psql "<DATABASE_URL>" -f database/schema/initial_schema.sql
  psql "<DATABASE_URL>" -f database/schema/knowledge_base_seed.sql
  ```

### 3. Deploy the AI Microservice
- Create a new **Web Service** from your GitHub repo.
- **Root Directory**: `ai-service`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -w 2 -b 0.0.0.0:$PORT --chdir src main:app --timeout 60`
- **Environment Variables**:
  - `LLM_PROVIDER`: `gemini`
  - `GOOGLE_API_KEY`: `<Your Google Gemini API Key>`
  - `LLM_MODEL`: `models/gemini-3.6-flash`
  - `AI_SERVICE_PORT`: `5001`
- Note the public URL (e.g., `https://fpa-ai-service.onrender.com`).

### 4. Deploy the Backend & Web App
- Create a new **Web Service** from your GitHub repo.
- **Build Command**:
  ```bash
  cd frontend && npm install && npm run build && cd ../backend && npm install
  ```
- **Start Command**:
  ```bash
  cd backend && node src/server.js
  ```
- **Environment Variables**:
  - `NODE_ENV`: `production`
  - `PORT`: `5000` (or leave default for PaaS)
  - `DATABASE_URL`: `<Your Managed PostgreSQL URL>`
  - `AI_SERVICE_URL`: `https://fpa-ai-service.onrender.com`
  - `JWT_SECRET`: `<Generate a random 32+ character secret>`
  - `ADMIN_EMAIL`: `joshua@ajala.com`
- Once deployed, your web application will be live at `https://fpa-assistant.onrender.com`.

---

## Option 2: Deploy to an Ubuntu Cloud VPS (DigitalOcean, AWS, Linode, Campus Server)

This gives complete institutional control, high performance, and allows binding your institutional domain (e.g. `assistant.fedpolyado.edu.ng`).

### 1. Server Prerequisites
Launch an Ubuntu 22.04 or 24.04 server (minimum 2GB RAM) and install packages:
```bash
sudo apt update && sudo apt install -y nodejs npm python3 python3-pip python3-venv postgresql postgresql-contrib nginx certbot python3-certbot-nginx
```

### 2. Configure Database
```bash
sudo -u postgres psql
CREATE DATABASE educational_assistant;
CREATE USER fpa_user WITH ENCRYPTED PASSWORD 'StrongSecurePassword123!';
GRANT ALL PRIVILEGES ON DATABASE educational_assistant TO fpa_user;
\q

# Load schema and institutional seed
psql -U fpa_user -d educational_assistant -h localhost -f database/schema/initial_schema.sql
psql -U fpa_user -d educational_assistant -h localhost -f database/schema/knowledge_base_seed.sql
```

### 3. Setup Project & Seed Admin Account
```bash
# In backend/.env
DATABASE_URL=postgresql://fpa_user:StrongSecurePassword123!@localhost:5432/educational_assistant
ADMIN_EMAIL=joshua@ajala.com
GOOGLE_API_KEY=<Your Key>
LLM_PROVIDER=gemini
LLM_MODEL=models/gemini-3.6-flash

# Seed admin user
cd backend && node src/seed_admin.js
```

### 4. Setup Systemd Services (Automatic 24/7 Background Run)

Create `/etc/systemd/system/fpa-ai.service`:
```ini
[Unit]
Description=FPA Assistant - AI Microservice
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/var/www/fpa-assistant/ai-service
Environment="PYTHONPATH=src"
ExecStart=/var/www/fpa-assistant/ai-service/venv/bin/gunicorn -w 2 -b 127.0.0.1:5001 --chdir src main:app --timeout 60
Restart=always

[Install]
WantedBy=multi-user.target
```

Create `/etc/systemd/system/fpa-backend.service`:
```ini
[Unit]
Description=FPA Assistant - Web & Backend Service
After=network.target fpa-ai.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/var/www/fpa-assistant/backend
Environment=NODE_ENV=production
ExecStart=/usr/bin/node src/server.js
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start both services:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now fpa-ai
sudo systemctl enable --now fpa-backend
```

### 5. Configure Nginx & SSL (HTTPS)
Create `/etc/nginx/sites-available/fpa-assistant`:
```nginx
server {
    server_name assistant.fedpolyado.edu.ng;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site and activate free SSL:
```bash
sudo ln -s /etc/nginx/sites-available/fpa-assistant /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d assistant.fedpolyado.edu.ng
```

Your system is now live online with SSL at **`https://assistant.fedpolyado.edu.ng`**!

---

## Administrator Access
- **URL**: `https://your-domain.com/login`
- **Email**: `joshua@ajala.com`
- **Default Password**: `Admin123!` (Can be updated via the admin portal or database)
