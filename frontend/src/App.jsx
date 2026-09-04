import { useEffect, useState, useRef } from 'react';
import {
  BrowserRouter,
  Link,
  Navigate,
  Route,
  Routes,
  useNavigate,
  useLocation,
} from 'react-router-dom';
import axios from 'axios';
import './App.css';
import { parseInlineText } from './responseFormatting.jsx';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
});

api.interceptors.request.use((config) => {
  const token =
    localStorage.getItem('fpa_token') ||
    localStorage.getItem('ajala_token');

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// Inline SVG Icons for clean, professional look
const Icons = {
  Send: () => (
    <svg
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <line x1="22" y1="2" x2="11" y2="13"></line>
      <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
    </svg>
  ),

  Search: () => (
    <svg
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <circle cx="11" cy="11" r="8"></circle>
      <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
    </svg>
  ),

  ArrowRight: () => (
    <svg
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <line x1="5" y1="12" x2="19" y2="12"></line>
      <polyline points="12 5 19 12 12 19"></polyline>
    </svg>
  ),

  Check: () => (
    <svg
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <polyline points="20 6 9 17 4 12"></polyline>
    </svg>
  ),

  Lock: () => (
    <svg
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
    </svg>
  ),

  Plus: () => (
    <svg
      width="14"
      height="14"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <line x1="12" y1="5" x2="12" y2="19"></line>
      <line x1="5" y1="12" x2="19" y2="12"></line>
    </svg>
  ),
};

// Formatted response component
function FormattedText({ text }) {
  if (!text) return null;

  const lines = text.split('\n');
  const elements = [];

  let currentList = [];
  let listType = null;

  const flushList = () => {
    if (!currentList.length) return;

    const ListTag = listType === 'ol' ? 'ol' : 'ul';

    elements.push(
      <ListTag
        key={`${listType}-${elements.length}`}
        className={listType === 'ol' ? 'doc-ol' : 'doc-ul'}
      >
        {currentList.map((item, idx) => (
          <li key={idx}>{parseInlineText(item)}</li>
        ))}
      </ListTag>
    );

    currentList = [];
    listType = null;
  };

  lines.forEach((line, index) => {
    const trimmed = line.trim();

    if (!trimmed) {
      flushList();
      return;
    }

    const numMatch = trimmed.match(/^(\d+)\.\s+(.*)/);

    if (numMatch) {
      if (listType !== 'ol') {
        flushList();
        listType = 'ol';
      }

      currentList.push(numMatch[2]);
      return;
    }

    const bulletMatch = trimmed.match(/^[-*•]\s+(.*)/);

    if (bulletMatch) {
      if (listType !== 'ul') {
        flushList();
        listType = 'ul';
      }

      currentList.push(bulletMatch[1]);
      return;
    }

    flushList();

    if (trimmed.startsWith('### ')) {
      elements.push(
        <h4 key={index} className="doc-h4">
          {parseInlineText(trimmed.slice(4))}
        </h4>
      );
    } else if (trimmed.startsWith('## ')) {
      elements.push(
        <h3 key={index} className="doc-h3">
          {parseInlineText(trimmed.slice(3))}
        </h3>
      );
    } else if (trimmed.startsWith('# ')) {
      elements.push(
        <h2 key={index} className="doc-h2">
          {parseInlineText(trimmed.slice(2))}
        </h2>
      );
    } else {
      elements.push(
        <p key={index} className="doc-p">
          {parseInlineText(trimmed)}
        </p>
      );
    }
  });

  flushList();

  return <div className="formatted-doc">{elements}</div>;
}

function Header({ user, onLogout }) {
  const location = useLocation();

  return (
    <header className="site-header">
      <div className="site-header-inner">
        <Link to="/" className="site-brand">
          <div className="brand-crest-box">
            <span className="crest-letters">FPA</span>
          </div>

          <div className="brand-meta">
            <span className="brand-name">FPA Assistant</span>
            <span className="brand-inst">
              The Federal Polytechnic, Ado-Ekiti
            </span>
          </div>
        </Link>

        <nav className="site-nav">
          <Link
            to="/"
            className={`site-nav-item ${
              location.pathname === '/' ? 'active' : ''
            }`}
          >
            Overview
          </Link>

          <Link
            to="/chat"
            className={`site-nav-item ${
              location.pathname === '/chat' ? 'active' : ''
            }`}
          >
            Student Helpdesk
          </Link>

          {user?.role === 'admin' && (
            <Link
              to="/knowledge-base"
              className={`site-nav-item admin-tab ${
                location.pathname === '/knowledge-base' ? 'active' : ''
              }`}
            >
              Knowledge Base
            </Link>
          )}

          {user ? (
            <div className="auth-status-wrap">
              {user.role === 'admin' && (
                <Link
                  to="/admin"
                  className={`admin-portal-link ${
                    location.pathname === '/admin' ? 'active' : ''
                  }`}
                >
                  Admin Panel
                </Link>
              )}

              <div className="user-indicator" title={user.email}>
                <span className="user-circle">
                  {user.name?.charAt(0)?.toUpperCase() || 'U'}
                </span>

                <span className="user-shortname">
                  {user.name?.split(' ')[0] || 'User'}
                </span>
              </div>

              <button className="btn-logout" onClick={onLogout}>
                Sign Out
              </button>
            </div>
          ) : (
            <Link to="/login" className="btn-signin-nav">
              Sign In
            </Link>
          )}
        </nav>
      </div>
    </header>
  );
}

function Home() {
  const navigate = useNavigate();

  const handleConsult = (question) => {
    navigate('/chat', {
      state: {
        initialPrompt: question,
      },
    });
  };

  const serviceCategories = [
    {
      code: 'ADM',
      name: 'Admissions & Screening',
      desc: 'Entry requirements for National Diploma (ND) and Higher National Diploma (HND), Post-UTME screening, cut-off marks, and verification of admission lists.',
      sampleQuery:
        'What are the admission requirements for ND programmes?',
    },
    {
      code: 'FEE',
      name: 'Tuition & Payment Services',
      desc: 'Official schedule of institutional fees, invoice generation on the portal, Remita confirmation, and guidance for payment disputes.',
      sampleQuery:
        'How do I pay school fees and resolve payment issues?',
    },
    {
      code: 'REG',
      name: 'Course Registration',
      desc: 'Online semester registration procedures, credit unit limits, add/drop windows, departmental advisor sign-offs, and compliance deadlines.',
      sampleQuery:
        'How do I register my courses on the student portal?',
    },
    {
      code: 'EXM',
      name: 'Examinations & MIS Results',
      desc: 'Semester timetable releases, hall requirements, and accessing official approved grades on the Academic Results Management Portal (MIS).',
      sampleQuery:
        'Where can I check approved semester results on the MIS portal?',
    },
    {
      code: 'ACC',
      name: 'Hostel Accommodation',
      desc: 'Application criteria for on-campus student residential quarters, room space allocation, fee guidelines, and Student Affairs clearances.',
      sampleQuery:
        'How do I apply for campus hostel accommodation?',
    },
    {
      code: 'ICT',
      name: 'Portal & Technical Support',
      desc: 'Student account credential recovery, institution email management, and technical helpdesk contacts for academic systems.',
      sampleQuery:
        'I cannot log in to my student portal account. What should I do?',
    },
  ];

  return (
    <main className="landing-layout">
      <section className="institutional-hero">
        <div className="institution-flag">
          The Federal Polytechnic, Ado-Ekiti &middot; Directorate of
          Academic &amp; Student Affairs
        </div>

        <h1 className="hero-title">
          FPA Student Information &amp; Administrative Helpdesk
        </h1>

        <p className="hero-lead">
          Official institutional service assistant providing immediate,
          verified guidance on admissions, fee schedules, course
          registrations, examinations, and student services.
        </p>

        <div className="hero-cta-row">
          <Link to="/chat" className="btn-cta-primary">
            <span>Access Student Helpdesk</span>
            <Icons.ArrowRight />
          </Link>

          <div className="frequent-topics-wrap">
            <span className="topics-heading">Common inquiries:</span>

            <button
              className="topic-btn"
              onClick={() =>
                handleConsult(
                  'What are the admission requirements for ND programmes?'
                )
              }
            >
              ND Admission Requirements
            </button>

            <button
              className="topic-btn"
              onClick={() => handleConsult('How do I pay school fees?')}
            >
              School Fees &amp; Remita
            </button>

            <button
              className="topic-btn"
              onClick={() =>
                handleConsult('Where can I check my semester results?')
              }
            >
              MIS Semester Results
            </button>
          </div>
        </div>
      </section>

      <section className="directory-section">
        <div className="directory-header">
          <h2>Institutional Administrative Services</h2>

          <p>
            Select any category below to consult verified institutional
            guidelines or submit a query directly.
          </p>
        </div>

        <div className="directory-grid">
          {serviceCategories.map((cat) => (
            <article
              key={cat.code}
              className="directory-card"
              onClick={() => handleConsult(cat.sampleQuery)}
            >
              <div className="card-top-meta">
                <span className="cat-code">{cat.code}</span>

                <span className="card-action-cue">
                  Inquire <Icons.ArrowRight />
                </span>
              </div>

              <h3 className="card-title">{cat.name}</h3>

              <p className="card-text">{cat.desc}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="official-disclaimer-strip">
        <p>
          Official portal of The Federal Polytechnic, Ado-Ekiti (Ekiti
          State, Nigeria). For formal notices and direct circulars,
          reference the institutional website at{' '}
          <a
            href="https://fedpolyado.edu.ng"
            target="_blank"
            rel="noopener noreferrer"
          >
            fedpolyado.edu.ng
          </a>
          .
        </p>
      </section>
    </main>
  );
}

function Login({ setUser }) {
  const [mode, setMode] = useState('login');

  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
  });

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();

    setError('');
    setLoading(true);

    try {
      const { data } = await api.post(`/api/auth/${mode}`, form);

      localStorage.setItem('fpa_token', data.token);

      setUser(data.user);

      navigate(data.user.role === 'admin' ? '/admin' : '/chat');
    } catch (err) {
      setError(
        err.response?.data?.error ||
          'Authentication failed. Verify your email and password.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-canvas">
      <div className="auth-box">
        <div className="auth-header-strip">
          <span className="crest-small">FPA</span>
          <span>The Federal Polytechnic, Ado-Ekiti</span>
        </div>

        <h2>
          {mode === 'login'
            ? 'Institutional Sign In'
            : 'Register Student Account'}
        </h2>

        <p className="auth-caption">
          {mode === 'login'
            ? 'Sign in to access your saved session history and administrative records.'
            : 'Enter your name and institutional credentials to register.'}
        </p>

        <form className="auth-input-form" onSubmit={submit}>
          {mode === 'register' && (
            <div className="form-control">
              <label>Full Name</label>

              <input
                type="text"
                placeholder="Surname Firstname Middlename"
                required
                value={form.name}
                onChange={(e) =>
                  setForm({
                    ...form,
                    name: e.target.value,
                  })
                }
              />
            </div>
          )}

          <div className="form-control">
            <label>Email Address</label>

            <input
              type="email"
              placeholder="e.g. user@fedpolyado.edu.ng"
              required
              value={form.email}
              onChange={(e) =>
                setForm({
                  ...form,
                  email: e.target.value,
                })
              }
            />
          </div>

          <div className="form-control">
            <label>Password</label>

            <input
              type="password"
              placeholder="Minimum 8 characters"
              minLength="8"
              required
              value={form.password}
              onChange={(e) =>
                setForm({
                  ...form,
                  password: e.target.value,
                })
              }
            />
          </div>

          {error && <div className="auth-alert-box">{error}</div>}

          <button
            type="submit"
            className="btn-auth-action"
            disabled={loading}
          >
            {loading
              ? 'Processing...'
              : mode === 'login'
              ? 'Sign In to Portal'
              : 'Register Account'}
          </button>
        </form>

        <div className="auth-switch-row">
          <button
            type="button"
            className="btn-switch-mode"
            onClick={() => {
              setMode(mode === 'login' ? 'register' : 'login');
              setError('');
            }}
          >
            {mode === 'login'
              ? 'First time user? Create an account'
              : 'Already have an account? Sign in here'}
          </button>
        </div>
      </div>
    </main>
  );
}

function Chat({ user }) {
  const location = useLocation();

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const [loadingMessage, setLoadingMessage] = useState(
    'Consulting institutional records...'
  );

  const [conversationId, setConversationId] = useState(null);
  const [conversations, setConversations] = useState([]);
  const [feedbackSent, setFeedbackSent] = useState({});
  const [showHistory, setShowHistory] = useState(false);

  const messagesEndRef = useRef(null);
  const serviceWarmedRef = useRef(false);

  const starterQueries = [
    'What are the admission requirements for ND programmes?',
    'How do I register my courses online?',
    'How do I pay my school fees?',
    'Where can I check my semester results?',
    'What do I do if payment fails or is not confirmed?',
    'Where is the school located and how do I contact support?',
  ];

  const sleep = (ms) =>
    new Promise((resolve) => setTimeout(resolve, ms));

  const isColdStartError = (err) => {
    const status = err.response?.status;

    return (
      !err.response ||
      status === 500 ||
      status === 502 ||
      status === 503 ||
      status === 504 ||
      err.code === 'ECONNABORTED' ||
      err.code === 'ERR_NETWORK'
    );
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({
      behavior: 'smooth',
    });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  useEffect(() => {
    if (location.state?.initialPrompt) {
      send(location.state.initialPrompt);

      window.history.replaceState(
        {},
        document.title,
        window.location.pathname
      );
    }
  }, [location.state]);

  useEffect(() => {
    if (user) {
      api
        .get('/api/conversations')
        .then((r) =>
          setConversations(r.data.conversations || [])
        )
        .catch(() => setConversations([]));
    }
  }, [user, conversationId]);

  const loadConversation = async (id) => {
    setLoading(true);
    setLoadingMessage('Loading saved session...');

    try {
      const { data } = await api.get(
        `/api/conversations/${id}/messages`
      );

      const formatted = (data.messages || [])
        .map((m) => [
          {
            role: 'user',
            content: m.user_message,
          },
          {
            role: 'assistant',
            content: m.ai_response,
            messageId: m.id,
            intent: m.intent,
          },
        ])
        .flat();

      setMessages(formatted);
      setConversationId(id);
      setShowHistory(false);
    } catch {
      // Fallback
    } finally {
      setLoading(false);
      setLoadingMessage('Consulting institutional records...');
    }
  };

  const startNewTopic = () => {
    setConversationId(null);
    setMessages([]);
    setShowHistory(false);
  };

  const submitFeedback = async (messageId, rating) => {
    if (!messageId) return;

    try {
      await api.post('/api/chat/feedback', {
        messageId,
        rating,
      });

      setFeedbackSent((prev) => ({
        ...prev,
        [messageId]: rating,
      }));
    } catch {
      // Ignore feedback errors
    }
  };

  const send = async (queryText) => {
    const message = (queryText || input).trim();

    if (!message || loading) return;

    setMessages((prev) => [
      ...prev,
      {
        role: 'user',
        content: message,
      },
    ]);

    if (!queryText) {
      setInput('');
    }

    setLoading(true);
    setLoadingMessage('Connecting to institutional services...');

    try {
      /*
       * First request in a browser session:
       * wake the Render backend before submitting the actual
       * chat request.
       *
       * /health is read-only, so this is safe to call.
       */
      if (!serviceWarmedRef.current) {
        try {
          await api.get('/health', {
            timeout: 60000,
          });
        } catch {
          // Continue to the actual chat request.
        }

        serviceWarmedRef.current = true;
      }

      setLoadingMessage(
        'Consulting institutional records...'
      );

      let data;

      try {
        const response = await api.post(
          '/api/chat/message',
          {
            message,
            conversationId,
          },
          {
            timeout: 60000,
          }
        );

        data = response.data;
      } catch (err) {
        /*
         * Render free services may need time to wake up.
         * Retry once for connection/cold-start failures.
         */
        if (!isColdStartError(err)) {
          throw err;
        }

        setLoadingMessage(
          'The helpdesk is starting up. Please wait a moment...'
        );

        await sleep(3000);

        const response = await api.post(
          '/api/chat/message',
          {
            message,
            conversationId,
          },
          {
            timeout: 60000,
          }
        );

        data = response.data;
      }

      if (data.conversationId) {
        setConversationId(data.conversationId);
      }

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.response,
          messageId: data.messageId,
          intent: data.intent,
        },
      ]);
    } catch (err) {
      console.error('Chat request failed:', err);

      const status = err.response?.status;

      let errorMessage =
        'The institutional helpdesk is temporarily unavailable. Please try your question again in a few moments.';

      if (status === 401 || status === 403) {
        errorMessage =
          err.response?.data?.error ||
          'Your session has expired. Please sign in again.';
      } else if (status >= 400 && status < 500) {
        errorMessage =
          err.response?.data?.error ||
          'The helpdesk could not process that request.';
      }

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: errorMessage,
        },
      ]);
    } finally {
      setLoading(false);
      setLoadingMessage(
        'Consulting institutional records...'
      );
    }
  };

  return (
    <div className="desk-viewport">
      {user && (
        <aside
          className={`desk-sidebar ${
            showHistory ? 'sidebar-open' : ''
          }`}
        >
          <div className="desk-sidebar-header">
            <h3>Saved Sessions</h3>

            <button
              className="btn-new-topic"
              onClick={startNewTopic}
            >
              <Icons.Plus /> New
            </button>
          </div>

          <div className="desk-sidebar-content">
            {conversations.length === 0 ? (
              <p className="sidebar-empty-msg">
                No saved sessions.
              </p>
            ) : (
              conversations.map((c) => (
                <div
                  key={c.id}
                  className={`session-item ${
                    c.id === conversationId
                      ? 'session-item-selected'
                      : ''
                  }`}
                  onClick={() => loadConversation(c.id)}
                >
                  <span className="session-title">
                    {c.title || 'Session'}
                  </span>

                  <span className="session-date">
                    {new Date(
                      c.updated_at
                    ).toLocaleDateString([], {
                      month: 'short',
                      day: 'numeric',
                    })}
                  </span>
                </div>
              ))
            )}
          </div>
        </aside>
      )}

      <section className="desk-workspace">
        <div className="desk-topbar">
          <div className="desk-topbar-left">
            {user && (
              <button
                className="btn-toggle-sidebar"
                onClick={() =>
                  setShowHistory(!showHistory)
                }
              >
                {showHistory
                  ? 'Hide Sessions'
                  : 'Session History'}
              </button>
            )}

            <div className="desk-title-block">
              <h2>FPA Helpdesk Session</h2>

              <span className="desk-status-tag">
                Connected &middot; Federal Polytechnic,
                Ado-Ekiti
              </span>
            </div>
          </div>

          {conversationId && (
            <button
              className="btn-clear-session"
              onClick={startNewTopic}
            >
              + Start New Inquiry
            </button>
          )}
        </div>

        {!user && (
          <div className="guest-notice-strip">
            <span>
              Guest session active.{' '}
              <Link to="/login">Sign in</Link> to preserve
              your inquiry records.
            </span>
          </div>
        )}

        <div className="desk-thread">
          {messages.length === 0 ? (
            <div className="desk-empty-slate">
              <div className="slate-emblem">FPA</div>

              <h3>
                How can the institution assist you today?
              </h3>

              <p>
                Inquire regarding admissions, fees, course
                registrations, examinations, or student
                affairs.
              </p>

              <div className="starter-grid-wrap">
                <span className="starter-label">
                  Frequent administrative inquiries:
                </span>

                <div className="starter-queries-grid">
                  {starterQueries.map((q, idx) => (
                    <button
                      key={idx}
                      className="starter-query-button"
                      onClick={() => send(q)}
                    >
                      <span>{q}</span>
                      <Icons.ArrowRight />
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            messages.map((m, idx) => (
              <div
                key={idx}
                className={`dialog-entry ${
                  m.role === 'user'
                    ? 'dialog-user'
                    : 'dialog-helpdesk'
                }`}
              >
                <div className="dialog-speaker-badge">
                  {m.role === 'user'
                    ? 'Student'
                    : 'FPA Helpdesk'}
                </div>

                <div className="dialog-bubble">
                  <FormattedText text={m.content} />

                  {m.role === 'assistant' &&
                    m.messageId && (
                      <div className="dialog-feedback-row">
                        <span className="feedback-query">
                          Was this information accurate?
                        </span>

                        {feedbackSent[m.messageId] ? (
                          <span className="feedback-success-ack">
                            <Icons.Check /> Recorded
                          </span>
                        ) : (
                          <div className="feedback-btn-group">
                            <button
                              className="btn-feedback-action"
                              onClick={() =>
                                submitFeedback(
                                  m.messageId,
                                  5
                                )
                              }
                            >
                              Yes, accurate
                            </button>

                            <button
                              className="btn-feedback-action"
                              onClick={() =>
                                submitFeedback(
                                  m.messageId,
                                  1
                                )
                              }
                            >
                              Incomplete
                            </button>
                          </div>
                        )}
                      </div>
                    )}
                </div>
              </div>
            ))
          )}

          {loading && (
            <div className="dialog-entry dialog-helpdesk">
              <div className="dialog-speaker-badge">
                FPA Helpdesk
              </div>

              <div className="dialog-bubble loading-bubble">
                <span className="loading-pulse-text">
                  {loadingMessage}
                </span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="desk-input-dock">
          <form
            className="input-form-control"
            onSubmit={(e) => {
              e.preventDefault();
              send();
            }}
          >
            <input
              type="text"
              className="desk-query-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask an administrative question (e.g. ND admission criteria, school fees schedule)..."
              disabled={loading}
              autoFocus
            />

            <button
              type="submit"
              className="btn-desk-send"
              disabled={loading || !input.trim()}
            >
              <span>Submit</span>
              <Icons.Send />
            </button>
          </form>

          <div className="desk-disclaimer-note">
            Official administrative assistant for The
            Federal Polytechnic, Ado-Ekiti. Urgent notices
            are published on{' '}
            <a
              href="https://fedpolyado.edu.ng"
              target="_blank"
              rel="noreferrer"
            >
              fedpolyado.edu.ng
            </a>
            .
          </div>
        </div>
      </section>
    </div>
  );
}

// KNOWLEDGE BASE - ACCESSIBLE ONLY TO ADMIN USERS
function KnowledgeBase({ user }) {
  const [items, setItems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] =
    useState('');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get('/api/categories')
      .then((r) =>
        setCategories(r.data.categories || [])
      )
      .catch(() => {});
  }, []);

  useEffect(() => {
    setLoading(true);

    const params = {};

    if (search) {
      params.search = search;
    }

    if (selectedCategory) {
      params.category = selectedCategory;
    }

    api
      .get('/api/kb', { params })
      .then((r) => setItems(r.data.data || []))
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, [search, selectedCategory]);

  if (user?.role !== 'admin') {
    return <Navigate to="/chat" replace />;
  }

  return (
    <main className="kb-repository-layout">
      <div className="kb-repository-inner">
        <header className="kb-repo-header">
          <div className="repo-breadcrumb">
            <Link to="/admin">Admin Panel</Link> /{' '}
            <span>Knowledge Base Repository</span>
          </div>

          <h1>Institutional Knowledge Base</h1>

          <p>
            Internal directory of institutional Q&amp;A
            records utilized by the FPA Assistant.
            (Administrator Access Only)
          </p>
        </header>

        <div className="repo-filters-bar">
          <div className="repo-search-wrap">
            <Icons.Search />

            <input
              className="repo-search-input"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search across questions, answers, and tags..."
            />
          </div>

          <div className="repo-categories-row">
            <button
              className={`repo-cat-btn ${
                selectedCategory === ''
                  ? 'repo-cat-active'
                  : ''
              }`}
              onClick={() => setSelectedCategory('')}
            >
              All Categories ({items.length})
            </button>

            {categories.map((c) => (
              <button
                key={c.id}
                className={`repo-cat-btn ${
                  selectedCategory === c.name
                    ? 'repo-cat-active'
                    : ''
                }`}
                onClick={() =>
                  setSelectedCategory(c.name)
                }
              >
                {c.name}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="repo-state-loading">
            Retrieving repository records...
          </div>
        ) : items.length === 0 ? (
          <div className="repo-state-empty">
            <p>No matching knowledge entries found.</p>

            <button
              className="btn-clear-search"
              onClick={() => {
                setSearch('');
                setSelectedCategory('');
              }}
            >
              Reset Search Filter
            </button>
          </div>
        ) : (
          <div className="repo-cards-grid">
            {items.map((item) => (
              <article
                className="repo-entry-card"
                key={item.id}
              >
                <div className="entry-card-meta">
                  <span className="entry-cat-tag">
                    {item.category_name}
                  </span>

                  {item.source && (
                    <span className="entry-source-tag">
                      Source: {item.source}
                    </span>
                  )}
                </div>

                <h3 className="entry-card-question">
                  {item.question}
                </h3>

                <div className="entry-card-answer">
                  <FormattedText text={item.answer} />
                </div>

                {item.keywords && (
                  <div className="entry-card-keywords">
                    <strong>Keywords:</strong>{' '}
                    {item.keywords}
                  </div>
                )}
              </article>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}

function Admin({ user }) {
  const [items, setItems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [statusFilter, setStatusFilter] = useState('all');
  const [categoryFilter, setCategoryFilter] =
    useState('all');

  const initialForm = {
    categoryId: '',
    question: '',
    answer: '',
    keywords: '',
    source: '',
    status: 'active',
  };

  const [form, setForm] = useState(initialForm);
  const [formError, setFormError] = useState('');
  const [saving, setSaving] = useState(false);

  const loadData = async () => {
    setLoading(true);

    try {
      const [kbRes, catRes, statRes] =
        await Promise.all([
          api.get('/api/admin/kb'),
          api.get('/api/categories'),
          api.get('/api/admin/analytics'),
        ]);

      setItems(kbRes.data.data || []);
      setCategories(catRes.data.categories || []);
      setAnalytics(
        statRes.data.analytics || null
      );
    } catch {
      // Error
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user?.role === 'admin') {
      loadData();
    }
  }, [user]);

  if (user?.role !== 'admin') {
    return <Navigate to="/login" replace />;
  }

  const openCreateModal = () => {
    setEditingItem(null);

    setForm({
      ...initialForm,
      categoryId: categories[0]?.id || 1,
    });

    setFormError('');
    setShowModal(true);
  };

  const openEditModal = (item) => {
    setEditingItem(item);

    setForm({
      categoryId: item.category_id,
      question: item.question,
      answer: item.answer,
      keywords: item.keywords || '',
      source: item.source || '',
      status: item.status || 'active',
    });

    setFormError('');
    setShowModal(true);
  };

  const handleSave = async (e) => {
    e.preventDefault();

    setFormError('');
    setSaving(true);

    try {
      if (editingItem) {
        await api.put(
          `/api/admin/kb/${editingItem.id}`,
          form
        );
      } else {
        await api.post('/api/admin/kb', form);
      }

      setShowModal(false);
      loadData();
    } catch (err) {
      setFormError(
        err.response?.data?.error ||
          'Failed to update knowledge record.'
      );
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id, question) => {
    if (
      window.confirm(
        `Confirm deletion of the following record?\n\n"${question}"`
      )
    ) {
      try {
        await api.delete(`/api/admin/kb/${id}`);
        loadData();
      } catch {
        alert('Failed to delete entry');
      }
    }
  };

  const filteredItems = items.filter((i) => {
    if (
      statusFilter !== 'all' &&
      i.status !== statusFilter
    ) {
      return false;
    }

    if (
      categoryFilter !== 'all' &&
      i.category_id.toString() !== categoryFilter
    ) {
      return false;
    }

    return true;
  });

  return (
    <main className="admin-portal-layout">
      <div className="admin-portal-inner">
        <header className="admin-header-row">
          <div>
            <span className="admin-scope-badge">
              Institutional Administration
            </span>

            <h1>FPA Assistant Management</h1>

            <p>
              Knowledge repository maintenance,
              operational metrics, and institutional
              updates.
            </p>
          </div>

          <div className="admin-controls-group">
            <Link
              to="/knowledge-base"
              className="btn-view-repository"
            >
              View Repository
            </Link>

            <button
              className="btn-create-entry"
              onClick={openCreateModal}
            >
              <Icons.Plus /> Add Knowledge Entry
            </button>
          </div>
        </header>

        {analytics && (
          <section className="admin-stats-grid">
            <div className="stat-box">
              <span className="stat-label">
                Registered Users
              </span>

              <span className="stat-value">
                {analytics.total_users}
              </span>

              <span className="stat-detail">
                Student accounts
              </span>
            </div>

            <div className="stat-box">
              <span className="stat-label">
                Total Sessions
              </span>

              <span className="stat-value">
                {analytics.total_conversations}
              </span>

              <span className="stat-detail">
                Inquiry sessions
              </span>
            </div>

            <div className="stat-box">
              <span className="stat-label">
                Queries Processed
              </span>

              <span className="stat-value">
                {analytics.total_queries}
              </span>

              <span className="stat-detail">
                Helpdesk answers provided
              </span>
            </div>

            <div className="stat-box">
              <span className="stat-label">
                Active Knowledge Records
              </span>

              <span className="stat-value">
                {analytics.active_kb_entries}
              </span>

              <span className="stat-detail">
                Verified data entries
              </span>
            </div>
          </section>
        )}

        <div className="admin-table-bar">
          <div className="table-filter-pair">
            <div className="select-field">
              <label>Category:</label>

              <select
                value={categoryFilter}
                onChange={(e) =>
                  setCategoryFilter(e.target.value)
                }
              >
                <option value="all">
                  All Categories
                </option>

                {categories.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="select-field">
              <label>Status:</label>

              <select
                value={statusFilter}
                onChange={(e) =>
                  setStatusFilter(e.target.value)
                }
              >
                <option value="all">
                  All Statuses
                </option>

                <option value="active">Active</option>
                <option value="inactive">
                  Inactive
                </option>
              </select>
            </div>
          </div>

          <div className="table-count-tag">
            {filteredItems.length} records displayed
          </div>
        </div>

        <div className="admin-table-frame">
          <table className="admin-grid-table">
            <thead>
              <tr>
                <th>Category</th>
                <th>Inquiry &amp; Content</th>
                <th>Source</th>
                <th>Status</th>
                <th>Modified</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              {filteredItems.map((item) => (
                <tr key={item.id}>
                  <td>
                    <span className="tag-category-pill">
                      {item.category_name}
                    </span>
                  </td>

                  <td className="col-question-content">
                    <strong className="entry-q-title">
                      {item.question}
                    </strong>

                    <p className="entry-q-preview">
                      {item.answer.slice(0, 110)}...
                    </p>
                  </td>

                  <td className="col-source">
                    {item.source || '—'}
                  </td>

                  <td>
                    <span
                      className={`status-badge ${
                        item.status === 'active'
                          ? 'badge-live'
                          : 'badge-disabled'
                      }`}
                    >
                      {item.status}
                    </span>
                  </td>

                  <td className="col-date">
                    {new Date(
                      item.updated_at
                    ).toLocaleDateString()}
                  </td>

                  <td className="col-actions">
                    <button
                      className="btn-table-edit"
                      onClick={() =>
                        openEditModal(item)
                      }
                    >
                      Edit
                    </button>

                    <button
                      className="btn-table-delete"
                      onClick={() =>
                        handleDelete(
                          item.id,
                          item.question
                        )
                      }
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {showModal && (
          <div
            className="modal-veil"
            onClick={() => setShowModal(false)}
          >
            <div
              className="modal-dialog"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="modal-dialog-header">
                <h3>
                  {editingItem
                    ? 'Edit Knowledge Base Entry'
                    : 'Create Knowledge Base Entry'}
                </h3>

                <button
                  className="btn-close-modal"
                  onClick={() =>
                    setShowModal(false)
                  }
                  aria-label="Close modal"
                >
                  ✕
                </button>
              </div>

              <form
                className="modal-form-content"
                onSubmit={handleSave}
              >
                <div className="form-row-field">
                  <label>Service Category *</label>

                  <select
                    required
                    value={form.categoryId}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        categoryId: e.target.value,
                      })
                    }
                  >
                    {categories.map((c) => (
                      <option
                        key={c.id}
                        value={c.id}
                      >
                        {c.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-row-field">
                  <label>Question / Title *</label>

                  <input
                    required
                    placeholder="e.g. What are the admission requirements for ND programmes?"
                    value={form.question}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        question: e.target.value,
                      })
                    }
                  />
                </div>

                <div className="form-row-field">
                  <label>
                    Official Answer (Markdown
                    formatting supported) *
                  </label>

                  <textarea
                    required
                    rows="6"
                    placeholder="Verified institutional guidance..."
                    value={form.answer}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        answer: e.target.value,
                      })
                    }
                  />
                </div>

                <div className="form-two-col">
                  <div className="form-row-field">
                    <label>
                      Keywords (comma separated)
                    </label>

                    <input
                      placeholder="admission, requirements, nd"
                      value={form.keywords}
                      onChange={(e) =>
                        setForm({
                          ...form,
                          keywords: e.target.value,
                        })
                      }
                    />
                  </div>

                  <div className="form-row-field">
                    <label>Source Reference</label>

                    <input
                      placeholder="e.g. Admissions Office Official Guide"
                      value={form.source}
                      onChange={(e) =>
                        setForm({
                          ...form,
                          source: e.target.value,
                        })
                      }
                    />
                  </div>
                </div>

                <div className="form-row-field">
                  <label>Status</label>

                  <select
                    value={form.status}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        status: e.target.value,
                      })
                    }
                  >
                    <option value="active">
                      Active (available in queries)
                    </option>

                    <option value="inactive">
                      Inactive
                    </option>
                  </select>
                </div>

                {formError && (
                  <div className="modal-alert-error">
                    {formError}
                  </div>
                )}

                <div className="modal-button-strip">
                  <button
                    type="button"
                    className="btn-modal-dismiss"
                    onClick={() =>
                      setShowModal(false)
                    }
                  >
                    Cancel
                  </button>

                  <button
                    type="submit"
                    className="btn-modal-confirm"
                    disabled={saving}
                  >
                    {saving
                      ? 'Saving...'
                      : editingItem
                      ? 'Save Updates'
                      : 'Add Entry'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}

function Shell() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token =
      localStorage.getItem('fpa_token') ||
      localStorage.getItem('ajala_token');

    if (token) {
      api
        .get('/api/auth/me')
        .then((r) => setUser(r.data.user))
        .catch(() => {
          localStorage.removeItem('fpa_token');
          localStorage.removeItem('ajala_token');
        });
    }
  }, []);

  const logout = () => {
    localStorage.removeItem('fpa_token');
    localStorage.removeItem('ajala_token');
    setUser(null);
  };

  return (
    <div className="fpa-shell">
      <Header user={user} onLogout={logout} />

      <Routes>
        <Route path="/" element={<Home />} />

        <Route
          path="/chat"
          element={<Chat user={user} />}
        />

        <Route
          path="/knowledge-base"
          element={
            user?.role === 'admin' ? (
              <KnowledgeBase user={user} />
            ) : (
              <Navigate to="/chat" replace />
            )
          }
        />

        <Route
          path="/login"
          element={<Login setUser={setUser} />}
        />

        <Route
          path="/admin"
          element={<Admin user={user} />}
        />

        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />
      </Routes>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <Shell />
    </BrowserRouter>
  );
}