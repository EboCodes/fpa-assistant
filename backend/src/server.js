const express = require("express"),
  cors = require("cors"),
  helmet = require("helmet"),
  dotenv = require("dotenv"),
  axios = require("axios"),
  bcrypt = require("bcryptjs"),
  jwt = require("jsonwebtoken"),
  pgp = require("pg-promise"),
  path = require("path"),
  fs = require("fs");
dotenv.config();
const app = express(),
  PORT = process.env.PORT || 5000,
  db = pgp()(
    process.env.DATABASE_URL ||
      "postgresql://postgres:postgres@localhost:5432/educational_assistant",
  ),
  secret = process.env.JWT_SECRET || "development-only-change-me";
app.use(helmet({ contentSecurityPolicy: false }));
app.use(
  cors({
    origin: process.env.CLIENT_URL || "http://localhost:5173",
    credentials: true,
  }),
);
app.use(express.json());
const wrap = (fn) => (req, res, next) =>
    Promise.resolve(fn(req, res, next)).catch(next),
  safe = "id,name,email,role,created_at",
  token = (user) =>
    jwt.sign({ id: user.id, role: user.role, email: user.email }, secret, {
      expiresIn: process.env.JWT_EXPIRY || "7d",
    });
const auth = (req, res, next) => {
  try {
    req.user = jwt.verify(
      req.headers.authorization?.replace(/^Bearer\s+/i, ""),
      secret,
    );
    next();
  } catch {
    return res.status(401).json({ error: "Authentication required" });
  }
};
const optionalAuth = (req, res, next) => {
  const value = req.headers.authorization?.replace(/^Bearer\s+/i, "");
  if (value) {
    try {
      req.user = jwt.verify(value, secret);
    } catch {}
  }
  next();
};
const admin = [
  auth,
  (req, res, next) =>
    req.user.role === "admin"
      ? next()
      : res.status(403).json({ error: "Administrator access required" }),
];
app.get("/health", (req, res) =>
  res.json({ status: "API is running", timestamp: new Date() }),
);
app.post(
  "/api/auth/register",
  wrap(async (req, res) => {
    let { name, email, password } = req.body;
    if (!name?.trim() || !email?.trim() || !password || password.length < 8)
      return res.status(400).json({
        error: "Name, email, and an 8-character password are required",
      });
    email = email.trim().toLowerCase();
    const admins = (process.env.ADMIN_EMAILS || process.env.ADMIN_EMAIL || "")
        .split(",")
        .map((x) => x.trim().toLowerCase()),
      role = admins.includes(email) ? "admin" : "student",
      user = await db.one(
        `INSERT INTO users(name,email,password,role) VALUES($1,$2,$3,$4) RETURNING ${safe}`,
        [name.trim(), email, await bcrypt.hash(password, 12), role],
      );
    res.status(201).json({ token: token(user), user });
  }),
);
app.post(
  "/api/auth/login",
  wrap(async (req, res) => {
    const user = await db.oneOrNone("SELECT * FROM users WHERE email=$1", [
      req.body.email?.trim().toLowerCase(),
    ]);
    if (
      !user ||
      !(await bcrypt.compare(req.body.password || "", user.password))
    )
      return res.status(401).json({ error: "Invalid email or password" });
    const { password, ...publicUser } = user;
    res.json({ token: token(user), user: publicUser });
  }),
);
app.get(
  "/api/auth/me",
  auth,
  wrap(async (req, res) =>
    res.json({
      user: await db.one(`SELECT ${safe} FROM users WHERE id=$1`, [
        req.user.id,
      ]),
    }),
  ),
);
app.get(
  "/api/categories",
  wrap(async (req, res) =>
    res.json({
      success: true,
      categories: await db.any("SELECT * FROM categories ORDER BY name"),
    }),
  ),
);
app.get(
  "/api/kb",
  wrap(async (req, res) => {
    let q =
        "SELECT kb.*,c.name category_name FROM knowledge_base kb JOIN categories c ON c.id=kb.category_id WHERE kb.status=$1",
      v = ["active"];
    if (req.query.category) {
      v.push(req.query.category);
      q += ` AND (c.name=$${v.length} OR kb.category_id::text=$${v.length})`;
    }
    if (req.query.search) {
      v.push(`%${req.query.search}%`);
      q += ` AND (kb.question ILIKE $${v.length} OR kb.answer ILIKE $${v.length} OR kb.keywords ILIKE $${v.length})`;
    }
    const data = await db.any(q + " ORDER BY kb.updated_at DESC", v);
    res.json({ success: true, count: data.length, data });
  }),
);
app.get(
  "/api/conversations",
  auth,
  wrap(async (req, res) =>
    res.json({
      conversations: await db.any(
        "SELECT * FROM conversations WHERE user_id=$1 ORDER BY updated_at DESC",
        [req.user.id],
      ),
    }),
  ),
);
app.get(
  "/api/conversations/:id/messages",
  auth,
  wrap(async (req, res) => {
    const c = await db.oneOrNone(
      "SELECT id FROM conversations WHERE id=$1 AND user_id=$2",
      [req.params.id, req.user.id],
    );
    if (!c) return res.status(404).json({ error: "Conversation not found" });
    res.json({
      messages: await db.any(
        "SELECT * FROM chat_messages WHERE conversation_id=$1 ORDER BY created_at",
        [c.id],
      ),
    });
  }),
);
app.post(
  "/api/chat/message",
  optionalAuth,
  wrap(async (req, res) => {
    const { message, conversationId, category } = req.body;
    if (!message?.trim())
      return res.status(400).json({ error: "Message cannot be empty" });
    let c = null,
      history = [];
    if (req.user) {
      c =
        conversationId &&
        (await db.oneOrNone(
          "SELECT * FROM conversations WHERE id=$1 AND user_id=$2",
          [conversationId, req.user.id],
        ));
      if (!c)
        c = await db.one(
          "INSERT INTO conversations(user_id,title) VALUES($1,$2) RETURNING *",
          [req.user.id, message.trim().slice(0, 80)],
        );
      history = await db.any(
        "SELECT user_message,ai_response FROM chat_messages WHERE conversation_id=$1 ORDER BY created_at DESC LIMIT 6",
        [c.id],
      );
    }
    const ai = await axios.post(
        `${process.env.AI_SERVICE_URL || "http://localhost:5001"}/api/process`,
        {
          message: message.trim(),
          conversationId: c?.id,
          context: { category, history: history.reverse() },
        },
        { timeout: 45000 },
      ),
      p = ai.data || {},
      response = p.response || "I could not generate a response right now.";
    let messageId = null;
    if (c) {
      const msg = await db.one(
        "INSERT INTO chat_messages(conversation_id,user_message,ai_response,intent,confidence_score) VALUES($1,$2,$3,$4,$5) RETURNING id",
        [c.id, message.trim(), response, p.intent, p.confidence],
      );
      messageId = msg.id;
      await db.none(
        "UPDATE conversations SET updated_at=CURRENT_TIMESTAMP WHERE id=$1",
        [c.id],
      );
    }
    res.json({
      success: true,
      conversationId: c?.id || null,
      messageId,
      response,
      sources: p.sources || [],
      response_mode: p.response_mode || "institutional",
      intent: p.intent || null,
      confidence: p.confidence || null,
      suggested_kb_entries: p.suggested_kb_entries || [],
    });
  }),
);
app.post(
  "/api/chat/feedback",
  optionalAuth,
  wrap(async (req, res) => {
    const { messageId, rating, feedbackText } = req.body;
    if (!messageId && !rating) {
      return res.status(400).json({ error: "Message ID and rating are required" });
    }
    const cleanRating = Math.max(1, Math.min(5, parseInt(rating, 10) || 5));
    let inserted = null;
    if (messageId) {
      inserted = await db.oneOrNone(
        "INSERT INTO feedback(message_id, user_id, rating, feedback_text) VALUES($1, $2, $3, $4) RETURNING *",
        [messageId, req.user?.id || null, cleanRating, (feedbackText || "").trim().slice(0, 500)],
      );
    }
    res.json({ success: true, feedback: inserted });
  }),
);
app.get(
  "/api/admin/kb",
  ...admin,
  wrap(async (req, res) =>
    res.json({
      data: await db.any(
        "SELECT kb.*,c.name category_name FROM knowledge_base kb JOIN categories c ON c.id=kb.category_id ORDER BY kb.updated_at DESC",
      ),
    }),
  ),
);
app.post(
  "/api/admin/kb",
  ...admin,
  wrap(async (req, res) => {
    const {
      categoryId,
      question,
      answer,
      keywords = "",
      source = "",
      status = "active",
    } = req.body;
    if (!categoryId || !question?.trim() || !answer?.trim())
      return res
        .status(400)
        .json({ error: "Category, question and answer are required" });
    res.status(201).json({
      data: await db.one(
        "INSERT INTO knowledge_base(category_id,question,answer,keywords,source,created_by,status) VALUES($1,$2,$3,$4,$5,$6,$7) RETURNING *",
        [
          categoryId,
          question.trim(),
          answer.trim(),
          keywords,
          source,
          req.user.id,
          status,
        ],
      ),
    });
  }),
);
app.put(
  "/api/admin/kb/:id",
  ...admin,
  wrap(async (req, res) => {
    const {
      categoryId,
      question,
      answer,
      keywords = "",
      source = "",
      status = "active",
    } = req.body;
    const data = await db.oneOrNone(
      "UPDATE knowledge_base SET category_id=$1,question=$2,answer=$3,keywords=$4,source=$5,status=$6,updated_at=CURRENT_TIMESTAMP WHERE id=$7 RETURNING *",
      [categoryId, question, answer, keywords, source, status, req.params.id],
    );
    if (!data) return res.status(404).json({ error: "Entry not found" });
    res.json({ data });
  }),
);
app.delete(
  "/api/admin/kb/:id",
  ...admin,
  wrap(async (req, res) => {
    await db.none("DELETE FROM knowledge_base WHERE id=$1", [req.params.id]);
    res.json({ success: true });
  }),
);
app.get(
  "/api/admin/analytics",
  ...admin,
  wrap(async (req, res) =>
    res.json({
      analytics: await db.one(
        "SELECT (SELECT COUNT(*) FROM users) total_users,(SELECT COUNT(*) FROM conversations) total_conversations,(SELECT COUNT(*) FROM chat_messages) total_queries,(SELECT COUNT(*) FROM knowledge_base WHERE status='active') active_kb_entries",
      ),
    }),
  ),
);
const distPath = path.join(__dirname, "../../frontend/dist");
if (fs.existsSync(distPath)) {
  app.use(express.static(distPath));
  app.get("*", (req, res, next) => {
    if (req.path.startsWith("/api") || req.path.startsWith("/health")) {
      return next();
    }
    res.sendFile(path.join(distPath, "index.html"));
  });
}

app.use((req, res) => res.status(404).json({ error: "Route not found" }));
app.use((err, req, res, next) => {
  console.error(err);
  const aiUnavailable = err.isAxiosError && !err.response;
  res.status(err.code === "23505" ? 409 : aiUnavailable ? 503 : 500).json({
    error:
      err.code === "23505"
        ? "That record already exists"
        : aiUnavailable
          ? "The AI service is unavailable. Start the AI service and try again."
          : "Internal server error",
  });
});
if (require.main === module) {
  db.one("SELECT 1").catch((e) =>
    console.error("Database connection failed:", e.message),
  );
  const server = app.listen(PORT, () => console.log(`Backend running on :${PORT}`));
  const shutdown = () => {
    console.log("Shutting down backend...");
    server.close(() => {
      db.$pool.end();
      process.exit(0);
    });
  };
  process.on("SIGINT", shutdown);
  process.on("SIGTERM", shutdown);
}
module.exports = app;
