/**
 * Comprehensive End-to-End System Verification
 */

const axios = require('axios');

const API = 'http://localhost:5000';

async function runVerification() {
  console.log('==================================================');
  console.log('🔍 Starting Ajala Assistant Full Verification Suite');
  console.log('==================================================\n');

  let passed = 0;
  let failed = 0;

  const test = async (name, fn) => {
    try {
      await fn();
      console.log(`✅ PASS: ${name}`);
      passed++;
    } catch (err) {
      console.error(`❌ FAIL: ${name} ->`, err.response?.data || err.message);
      failed++;
    }
  };

  // 1. Health
  await test('Backend Health Endpoint (/health)', async () => {
    const res = await axios.get(`${API}/health`);
    if (res.data.status !== 'API is running') throw new Error('Invalid status');
  });

  await test('AI Microservice Health (direct :5001)', async () => {
    const res = await axios.get(`http://localhost:5001/health`);
    if (!res.data.status.includes('running')) throw new Error('AI service not running');
  });

  // 2. Categories
  await test('Fetch Categories (/api/categories)', async () => {
    const res = await axios.get(`${API}/api/categories`);
    if (!res.data.categories || res.data.categories.length < 10) throw new Error('Missing categories');
  });

  // 3. Knowledge Base
  await test('Query Knowledge Base (/api/kb)', async () => {
    const res = await axios.get(`${API}/api/kb?category=Admission`);
    if (!res.data.data || res.data.data.length === 0) throw new Error('No admission KB entries found');
  });

  // 4. Admin Authentication
  let adminToken = '';
  await test('Admin Login (joshua@ajala.com)', async () => {
    const res = await axios.post(`${API}/api/auth/login`, {
      email: 'joshua@ajala.com',
      password: 'Admin123!',
    });
    if (!res.data.token || res.data.user.role !== 'admin') throw new Error('Admin auth failed');
    adminToken = res.data.token;
  });

  // 5. Admin Analytics
  await test('Admin Analytics (/api/admin/analytics)', async () => {
    const res = await axios.get(`${API}/api/admin/analytics`, {
      headers: { Authorization: `Bearer ${adminToken}` },
    });
    if (!res.data.analytics || typeof res.data.analytics.total_users !== 'string') {
      throw new Error('Invalid analytics response');
    }
    console.log('   Metrics:', res.data.analytics);
  });

  // 6. Admin KB CRUD
  let createdId = null;
  await test('Admin Create KB Entry (POST /api/admin/kb)', async () => {
    const res = await axios.post(
      `${API}/api/admin/kb`,
      {
        categoryId: 1,
        question: `Test Admission Question ${Date.now()}`,
        answer: 'Test verified response for institutional verification.',
        keywords: 'test, verification',
        source: 'Automated Test Suite',
        status: 'active',
      },
      { headers: { Authorization: `Bearer ${adminToken}` } },
    );
    if (!res.data.data?.id) throw new Error('Failed to create KB entry');
    createdId = res.data.data.id;
  });

  await test('Admin Update KB Entry (PUT /api/admin/kb/:id)', async () => {
    const res = await axios.put(
      `${API}/api/admin/kb/${createdId}`,
      {
        categoryId: 1,
        question: `Updated Admission Question ${createdId}`,
        answer: 'Updated verified answer.',
        keywords: 'test, updated',
        source: 'Updated Source',
        status: 'active',
      },
      { headers: { Authorization: `Bearer ${adminToken}` } },
    );
    if (res.data.data?.answer !== 'Updated verified answer.') throw new Error('Update failed');
  });

  await test('Admin Delete KB Entry (DELETE /api/admin/kb/:id)', async () => {
    const res = await axios.delete(`${API}/api/admin/kb/${createdId}`, {
      headers: { Authorization: `Bearer ${adminToken}` },
    });
    if (!res.data.success) throw new Error('Delete failed');
  });

  // 7. Student Registration & Authenticated Conversation with Feedback
  let studentToken = '';
  const testEmail = `student_${Date.now()}@fedpolyado.edu.ng`;
  await test('Student Registration (/api/auth/register)', async () => {
    const res = await axios.post(`${API}/api/auth/register`, {
      name: 'Joshua Student',
      email: testEmail,
      password: 'Password123!',
    });
    if (!res.data.token || res.data.user.role !== 'student') throw new Error('Student registration failed');
    studentToken = res.data.token;
  });

  let conversationId = null;
  let messageId = null;
  await test('Authenticated Student Chat with Persistence (POST /api/chat/message)', async () => {
    const res = await axios.post(
      `${API}/api/chat/message`,
      {
        message: 'How do I register courses online?',
      },
      { headers: { Authorization: `Bearer ${studentToken}` } },
    );
    if (!res.data.conversationId || !res.data.response) throw new Error('Chat failed');
    conversationId = res.data.conversationId;
    messageId = res.data.messageId;
    console.log(`   Conversation ID: ${conversationId}, Message ID: ${messageId}`);
  });

  await test('Conversation History Retrieval (/api/conversations)', async () => {
    const res = await axios.get(`${API}/api/conversations`, {
      headers: { Authorization: `Bearer ${studentToken}` },
    });
    if (!res.data.conversations || res.data.conversations.length === 0) throw new Error('No conversations found');
  });

  await test('Submit Response Feedback (POST /api/chat/feedback)', async () => {
    const res = await axios.post(
      `${API}/api/chat/feedback`,
      {
        messageId,
        rating: 5,
        feedbackText: 'Very helpful and direct guidance!',
      },
      { headers: { Authorization: `Bearer ${studentToken}` } },
    );
    if (!res.data.success || !res.data.feedback) throw new Error('Feedback submission failed');
  });

  // 8. Static Web App
  await test('Static Frontend Application Serving (GET /)', async () => {
    const res = await axios.get(`${API}/`);
    if (!res.data.includes('FPA Assistant') && !res.data.includes('<div id="root">')) {
      throw new Error('Frontend index.html was not returned');
    }
  });

  console.log('\n==================================================');
  console.log(`Results: ${passed} Passed, ${failed} Failed`);
  console.log('==================================================');

  if (failed > 0) process.exit(1);
}

runVerification();
