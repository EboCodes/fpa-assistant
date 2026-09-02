-- Database Schema for Educational Service Assistant
-- Created for The Federal Polytechnic, Ado-Ekiti

-- ============================================
-- USERS TABLE
-- ============================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- CATEGORIES TABLE
-- ============================================
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Categories
INSERT INTO categories (name, description) VALUES
('Admission', 'Admission requirements, procedures, and guidelines'),
('Course Registration', 'Course registration procedures and deadlines'),
('School Fees', 'School fees, payment procedures, and deadlines'),
('Examination', 'Examination schedules, requirements, and regulations'),
('Academic Calendar', 'Academic dates, holidays, and important schedules'),
('Hostel Services', 'Hostel applications and accommodation information'),
('SIWES', 'Students Industrial Work Experience Scheme'),
('Library Services', 'Library registration, borrowing, and resources'),
('ICT Support', 'Student portal, login issues, and technical support'),
('Transcript Services', 'Transcript requests and procedures'),
('Graduation Requirements', 'Graduation procedures and clearance requirements');

-- ============================================
-- KNOWLEDGE BASE (Q&A) TABLE
-- ============================================
CREATE TABLE knowledge_base (
    id SERIAL PRIMARY KEY,
    category_id INT NOT NULL,
    question TEXT NOT NULL UNIQUE,
    answer TEXT NOT NULL,
    keywords VARCHAR(255),
    source VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- ============================================
-- EMBEDDINGS TABLE (for semantic search)
-- ============================================
CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    kb_id INT NOT NULL,
    question_embedding DOUBLE PRECISION[],
    answer_embedding DOUBLE PRECISION[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kb_id) REFERENCES knowledge_base(id) ON DELETE CASCADE
);

-- ============================================
-- CONVERSATIONS TABLE
-- ============================================
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INT,
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- CHAT MESSAGES TABLE
-- ============================================
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    conversation_id INT NOT NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    intent VARCHAR(100),
    confidence_score FLOAT,
    kb_used INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (kb_used) REFERENCES knowledge_base(id)
);

-- ============================================
-- USER FEEDBACK TABLE
-- ============================================
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    message_id INT NOT NULL,
    user_id INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    feedback_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (message_id) REFERENCES chat_messages(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ============================================
-- ANALYTICS TABLE
-- ============================================
CREATE TABLE analytics (
    id SERIAL PRIMARY KEY,
    total_queries INT DEFAULT 0,
    total_users INT DEFAULT 0,
    average_response_time FLOAT,
    queries_resolved INT DEFAULT 0,
    date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- ADMIN LOGS TABLE
-- ============================================
CREATE TABLE admin_logs (
    id SERIAL PRIMARY KEY,
    admin_id INT NOT NULL,
    action VARCHAR(100),
    description TEXT,
    affected_table VARCHAR(100),
    affected_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id)
);

-- ============================================
-- INDEXES for Performance
-- ============================================
CREATE INDEX idx_kb_category ON knowledge_base(category_id);
CREATE INDEX idx_kb_status ON knowledge_base(status);
CREATE INDEX idx_messages_conversation ON chat_messages(conversation_id);
CREATE INDEX idx_messages_kb ON chat_messages(kb_used);
CREATE INDEX idx_feedback_message ON feedback(message_id);
CREATE INDEX idx_conversations_user ON conversations(user_id);

-- ============================================
-- SAMPLE DATA
-- ============================================

-- Sample Knowledge Base Entry (Admission)
INSERT INTO knowledge_base (category_id, question, answer, keywords, source, status) VALUES
(1, 
 'What are the admission requirements for ND programme?',
 'To gain admission into the ND (National Diploma) programme at The Federal Polytechnic Ado-Ekiti, prospective students must have:\n1. O'' Level (SSCE/WAEC/NECO) with at least 5 credits in relevant subjects\n2. A valid JAMB score (minimum 120 points)\n3. Pass the Post-UTME screening exercise\n4. Provide all necessary documents as requested by the admission office.\n\nFor specific subject requirements, please contact the admission office or visit the main campus.',
 'admission,requirements,ND,JAMB,SSCE,documents',
 'Admission Office Official Guide',
 'active');

INSERT INTO knowledge_base (category_id, question, answer, keywords, source, status) VALUES
(2,
 'How do I register my courses online?',
 'Course registration is done through the Student Information System (SIS) portal. Follow these steps:\n1. Log in to the portal using your student ID and password\n2. Navigate to "Academic" → "Course Registration"\n3. Select your level and programme\n4. Choose your courses based on your department''s requirements\n5. Review your selections carefully\n6. Click "Submit Registration"\n7. Print your registration receipt for your records\n\nRegistration is usually open during the first two weeks of each semester. Contact your department if you face any issues.',
 'course,registration,portal,SIS,online,courses',
 'Academic Affairs Office',
 'active');

INSERT INTO knowledge_base (category_id, question, answer, keywords, source, status) VALUES
(3,
 'What is the current school fee for ND 1 students?',
 'School fees vary by programme and level. For the most current ND 1 tuition fees, please:\n1. Log into the student portal\n2. Check your student account dashboard\n3. Or visit the Bursary Department during office hours\n4. Email: bursary@fedpolyado.edu.ng\n\nPayment should be made through the approved payment channels only. Keep your receipt for records.',
 'school fee,fees,payment,ND,tuition,cost',
 'Bursary Department',
 'active');

INSERT INTO knowledge_base (category_id, question, answer, keywords, source, status) VALUES
(4,
 'When are the examination schedules released?',
 'Examination schedules for each semester are typically released 2-3 weeks before the examination period begins. \n\nYou can view the schedule by:\n1. Logging into the Student Information System (SIS)\n2. Navigating to "Academic" → "Examination Schedule"\n3. Visiting the Examination Office notice board\n4. Checking your department''s official announcements\n\nMake sure to note your exam dates, venues, and times. Arrive 15 minutes early on exam day.',
 'examination,exam,schedule,timetable,dates,exam venue',
 'Examination Office',
 'active');
