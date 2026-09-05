-- ============================================
-- KNOWLEDGE CANDIDATES TABLE (Web Discoveries Queue)
-- ============================================
CREATE TABLE IF NOT EXISTS knowledge_candidates (
    id SERIAL PRIMARY KEY,
    category_id INT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    source VARCHAR(255),
    source_url TEXT,
    confidence FLOAT DEFAULT 0.85,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    reviewed_by INT REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_candidates_status ON knowledge_candidates(status);
CREATE INDEX IF NOT EXISTS idx_candidates_category ON knowledge_candidates(category_id);
