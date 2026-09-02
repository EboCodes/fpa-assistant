/**
 * Admin User Seed Script
 * Ensures the default administrator account exists in the database.
 */

const dotenv = require("dotenv");
const bcrypt = require("bcryptjs");
const path = require("path");

dotenv.config({ path: path.join(__dirname, "../.env") });

const pgp = require("pg-promise")();

const db = pgp(
  process.env.DATABASE_URL ||
    "postgresql://postgres:ayoade2004@localhost:5432/educational_assistant",
);

async function seedAdmin() {
  const adminEmail = (process.env.ADMIN_EMAIL || "admin@fedpolyado.edu.ng").trim().toLowerCase();
  const adminName = process.env.ADMIN_NAME || "System Administrator";
  const defaultPassword = process.env.ADMIN_DEFAULT_PASSWORD || "Admin123!";

  console.log(`Checking admin user: ${adminEmail}...`);

  try {
    const existing = await db.oneOrNone("SELECT * FROM users WHERE email=$1", [adminEmail]);
    const hashedPassword = await bcrypt.hash(defaultPassword, 12);

    if (existing) {
      await db.none(
        "UPDATE users SET role='admin', password=$1, name=$2, updated_at=CURRENT_TIMESTAMP WHERE id=$3",
        [hashedPassword, adminName, existing.id]
      );
      console.log(`✅ Admin user '${adminEmail}' already existed. Credentials and role updated.`);
    } else {
      const newUser = await db.one(
        "INSERT INTO users(name, email, password, role) VALUES($1, $2, $3, 'admin') RETURNING id, name, email, role",
        [adminName, adminEmail, hashedPassword]
      );
      console.log(`✅ Admin user created successfully (ID: ${newUser.id}, Email: ${newUser.email})`);
    }

    console.log(`Admin login details:`);
    console.log(`  Email:    ${adminEmail}`);
    console.log(`  Password: ${defaultPassword}`);
  } catch (error) {
    console.error("❌ Failed to seed admin user:", error.message);
    process.exit(1);
  } finally {
    pgp.end();
  }
}

if (require.main === module) {
  seedAdmin();
}

module.exports = seedAdmin;
