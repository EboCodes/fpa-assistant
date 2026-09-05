# FPA Assistant - System Rollback & Disaster Recovery Guide
**The Federal Polytechnic, Ado-Ekiti**

This document provides a step-by-step operational guide to execute a **Rollback Sequence** in the event of a failed deployment, server crash, or unexpected production bug.

---

## 🎯 Overview of System Resilience

The **FPA Assistant** architecture is designed with **Multi-Tier Fault Tolerance**:
1. **Frontend Isolation (Vercel)**: Frontend UI issues can be reverted instantly without affecting database records or backend services.
2. **Backend API Isolation (Render)**: Microservices and Node.js APIs can be rolled back independently in 1 click.
3. **Database Schema Preservation**: Database queries use `IF NOT EXISTS` and parameterized queries so existing data is never wiped during code updates.

---

## ⚡ Method 1: Instant 1-Click Cloud Rollbacks (Zero Downtime)

### A. Vercel Frontend Rollback (~5 Seconds)
If a new frontend code update introduces a visual or JavaScript error on `https://fpa-edu-assistant.vercel.app`:

1. Log in to the [Vercel Dashboard](https://vercel.com).
2. Select the **`fpa-edu-assistant`** project.
3. Navigate to the **Deployments** tab.
4. Locate the **previous working deployment** (e.g. `27c4895` or `1b4102b`).
5. Click the **`...` (Three Dots)** button on the right side of that deployment card.
6. Click **Instant Rollback** ➔ Confirm.
7. *Vercel instantly routes 100% of live web traffic back to that working build in under 5 seconds.*

---

### B. Render Backend & AI Service Rollback (~30 Seconds)
If a backend deployment on `https://fpa-backend-s09g.onrender.com` or `https://fpa-ai-service.onrender.com` fails:

1. Log in to the [Render Dashboard](https://dashboard.render.com).
2. Select the service experiencing issues (**`fpa-backend`** or **`fpa-ai-service`**).
3. Click **Deploys** on the left menu.
4. Find the last **Successful Build** marked with a green checkmark.
5. Click the **`...` (Three Dots)** menu next to that build.
6. Select **Rollback to this deploy**.
7. *Render immediately boots the previous working container images.*

---

## 🐙 Method 2: Git Code Repository Rollback (Developer Mode)

If you need to revert code changes directly in the GitHub repository (`origin main`):

### Option A: Safe Revert (Recommended)
This creates a new commit that cleanly reverses breaking changes without rewriting commit history:

```bash
cd /home/francis/Downloads/Ajala

# Revert the latest commit
git revert HEAD -m "revert: rollback to previous stable release"

# Push to GitHub (Vercel and Render will auto-build the reverted stable state)
git push origin main
```

### Option B: Rollback to a Specific Working Commit
To reset the repository directly to a known good commit (e.g. `27c4895`):

```bash
# Fetch latest repository state
git fetch origin

# Hard reset your local branch to the target working commit
git reset --hard 27c4895

# Force push to GitHub
git push --force origin main
```

---

## 💾 Method 3: Database Backup & Recovery Strategy

### 1. Create a Pre-Deployment Database Backup
Before executing major database alterations, generate a snapshot of your PostgreSQL database:

```bash
# Dump complete database schema and data to a timestamped file
pg_dump "<DATABASE_URL>" > database_backup_$(date +%Y%m%d_%H%M%S).sql
```

### 2. Restore Database from Backup
If a database restoration is required:

```bash
# Restore entire database state from snapshot
psql "<DATABASE_URL>" < database_backup_20260905_143000.sql
```

---

## 🚨 Emergency 3-Step Action Checklist

If the live application experiences an outage:

1. **Step 1 — Check Live Status**: Run `node backend/src/e2e_verification.js` or visit `https://fpa-backend-s09g.onrender.com/health`.
2. **Step 2 — Trigger 1-Click Rollback**: Use the Vercel or Render dashboard to rollback to the last green deployment.
3. **Step 3 — Inspect Runtime Logs**: Review Render/Vercel build logs to identify the root cause before pushing new commits.
