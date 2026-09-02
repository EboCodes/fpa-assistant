# FPA Assistant - REST API Specification

Complete technical API reference for **FPA Assistant (The Federal Polytechnic, Ado-Ekiti)**.

---

## 📡 Base URLs & Ports

- **Web Application & Backend API**: `http://localhost:5000` (Production port)
- **AI Microservice**: `http://localhost:5001` (Internal Flask / Gunicorn service)
- **Vite Dev Server (Optional)**: `http://localhost:5173`

---

## 🔐 Authentication

Authentication is handled via JSON Web Tokens (JWT). When an endpoint requires authentication, include the Bearer token in the `Authorization` HTTP header:

```http
Authorization: Bearer <JWT_TOKEN>
```

Tokens are valid for 7 days and encode the user's `id`, `name`, `email`, and `role` (`student` or `admin`).

---

## 🛣️ Backend API Endpoints

### 1. System Health

#### `GET /health`
Checks backend service availability and PostgreSQL database connectivity.

- **Request**: `GET /health`
- **Response (200 OK)**:
```json
{
  "status": "API is running",
  "timestamp": "2026-09-02T20:52:25.011Z"
}
```

---

### 2. Authentication Endpoints

#### `POST /api/auth/register`
Creates a new student account. If the email matches `ADMIN_EMAIL` (e.g. `joshua@ajala.com`), the account is automatically granted `admin` privileges.

- **Request Body**:
```json
{
  "name": "Joshua Oluwaferanmi",
  "email": "student@fedpolyado.edu.ng",
  "password": "Password123!"
}
```
- **Response (201 Created)**:
```json
{
  "message": "User registered successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "name": "Joshua Oluwaferanmi",
    "email": "student@fedpolyado.edu.ng",
    "role": "student"
  }
}
```

#### `POST /api/auth/login`
Authenticates an existing user and issues a JWT.

- **Request Body**:
```json
{
  "email": "joshua@ajala.com",
  "password": "Admin123!"
}
```
- **Response (200 OK)**:
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 5,
    "name": "Administrator",
    "email": "joshua@ajala.com",
    "role": "admin"
  }
}
```

#### `GET /api/auth/me`
Fetches the current user profile from the validated token.
- **Headers**: `Authorization: Bearer <TOKEN>`
- **Response (200 OK)**:
```json
{
  "user": {
    "id": 5,
    "name": "Administrator",
    "email": "joshua@ajala.com",
    "role": "admin"
  }
}
```

---

### 3. Student Helpdesk & Chat

#### `POST /api/chat/message`
Processes a student inquiry through the AI microservice and records multi-turn conversation history.

- **Headers**: `Authorization: Bearer <TOKEN>` *(Optional; guests can chat without authentication)*
- **Request Body**:
```json
{
  "message": "What is the acceptance fee for newly admitted students?",
  "conversationId": 1
}
```
- **Response (200 OK)**:
```json
{
  "success": true,
  "conversationId": 1,
  "messageId": 24,
  "response": "The acceptance fee for newly admitted students at The Federal Polytechnic, Ado-Ekiti is **₦45,000** (exclusive of Remita service charges). \n\nTo pay your acceptance fee:\n1. Log in to the [FPA Student Portal](https://students.fedpolyado.edu.ng).\n2. Generate your payment invoice (RRR).\n3. Complete the payment online via Remita or take the RRR to any commercial bank.",
  "intent": "admission",
  "confidence": 0.5,
  "suggested_kb_entries": []
}
```

#### `POST /api/chat/feedback`
Records student feedback on an AI-generated answer.
- **Headers**: `Authorization: Bearer <TOKEN>` *(Optional)*
- **Request Body**:
```json
{
  "messageId": 24,
  "rating": 5,
  "feedbackText": "Very helpful and accurate information."
}
```
- **Response (200 OK)**:
```json
{
  "success": true,
  "feedback": {
    "id": 12,
    "message_id": 24,
    "rating": 5,
    "feedback_text": "Very helpful and accurate information.",
    "created_at": "2026-09-02T20:53:00.000Z"
  }
}
```

#### `GET /api/conversations`
Retrieves a list of prior conversation threads for the authenticated user.
- **Headers**: `Authorization: Bearer <TOKEN>`
- **Response (200 OK)**:
```json
{
  "conversations": [
    {
      "id": 1,
      "user_id": 2,
      "title": "What is the acceptance fee for newly admitted...",
      "created_at": "2026-09-02T17:50:00.000Z",
      "updated_at": "2026-09-02T20:51:00.000Z"
    }
  ]
}
```

#### `GET /api/conversations/:id/messages`
Fetches all historical user and assistant messages in a specific conversation thread.
- **Headers**: `Authorization: Bearer <TOKEN>`
- **Response (200 OK)**:
```json
{
  "messages": [
    {
      "id": 24,
      "conversation_id": 1,
      "user_message": "What is the acceptance fee for newly admitted students?",
      "ai_response": "The acceptance fee is ₦45,000...",
      "intent": "admission",
      "confidence": 0.5,
      "created_at": "2026-09-02T20:51:14.000Z"
    }
  ]
}
```

---

### 4. Knowledge Base & Categories

#### `GET /api/categories`
Retrieves all 11 institutional service categories.
- **Response (200 OK)**:
```json
{
  "categories": [
    { "id": 1, "name": "Admission", "description": "Questions about admission process and requirements" },
    { "id": 2, "name": "Course Registration", "description": "Questions about course registration and prerequisites" },
    { "id": 3, "name": "School Fees", "description": "Questions about fee structure and payment methods" },
    { "id": 4, "name": "Examination", "description": "Questions about examination schedules and grading" },
    { "id": 5, "name": "Academic Calendar", "description": "Questions about academic sessions and dates" },
    { "id": 6, "name": "Hostel Services", "description": "Questions about accommodation and hostel facilities" },
    { "id": 7, "name": "SIWES", "description": "Questions about industrial training and internship" },
    { "id": 8, "name": "Library Services", "description": "Questions about library resources and hours" },
    { "id": 9, "name": "ICT Support", "description": "Questions about portal access and email support" },
    { "id": 10, "name": "Transcript Services", "description": "Questions about transcript requests and processing" },
    { "id": 11, "name": "Graduation Requirements", "description": "Questions about graduation clearance and certs" }
  ]
}
```

#### `GET /api/kb`
Queries active knowledge base records. Supports keyword search and category filtering.
- **Query Parameters**:
  - `search`: Filter by keyword or text substring
  - `category`: Filter by category name string (e.g. `Admission`)
- **Response (200 OK)**:
```json
{
  "data": [
    {
      "id": 1,
      "category_id": 1,
      "category_name": "Admission",
      "question": "What is the acceptance fee for newly admitted students and how do I pay it?",
      "answer": "The acceptance fee for newly admitted students is ₦45,000...",
      "keywords": "acceptance fee, 45000, new students, admission, remita",
      "source": "Admissions Office Official Circular",
      "status": "active"
    }
  ]
}
```

---

### 5. Administrative Endpoints (Admin Role Required)

All administrative routes require a valid JWT with `role === 'admin'`.

#### `GET /api/admin/analytics`
Fetches live dashboard metrics.
- **Response (200 OK)**:
```json
{
  "analytics": {
    "total_users": "6",
    "total_conversations": "8",
    "total_queries": "8",
    "active_kb_entries": "55"
  }
}
```

#### `GET /api/admin/kb`
Returns all knowledge base records with category metadata for management in the table view.

#### `POST /api/admin/kb`
Creates a new verified knowledge base entry.
- **Request Body**:
```json
{
  "categoryId": 1,
  "question": "What is the deadline for 2026/2027 admission screening?",
  "answer": "The deadline is announced on the official portal...",
  "keywords": "deadline, admission, screening",
  "source": "Academic Affairs Circular",
  "status": "active"
}
```
- **Response (201 Created)**: Returns created record.

#### `PUT /api/admin/kb/:id`
Updates an existing knowledge base record.
- **Request Body**: `{ categoryId, question, answer, keywords, source, status }`
- **Response (200 OK)**: Returns updated record.

#### `DELETE /api/admin/kb/:id`
Deletes an existing knowledge base record.
- **Response (200 OK)**: `{ "success": true, "message": "Knowledge base entry deleted successfully" }`

---

## 🤖 Python AI Microservice (Port 5001)

### `GET /health`
Returns microservice health status:
```json
{ "status": "AI Service is running", "version": "1.0.0" }
```

### `POST /api/process`
Main NLP and response generation endpoint called internally by the Node.js backend.
- **Request Body**:
```json
{
  "message": "What is the acceptance fee for newly admitted students?",
  "conversationId": 1,
  "context": {
    "category": null,
    "history": [
      { "user_message": "Hi", "ai_response": "Hello! How can I assist you today?" }
    ]
  }
}
```
- **Response**:
```json
{
  "response": "The acceptance fee is ₦45,000...",
  "intent": "admission",
  "confidence": 0.5,
  "category_id": 1,
  "suggested_kb_entries": []
}
```
