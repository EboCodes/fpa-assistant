# FPA Assistant - Knowledge Base Repository Guide
**The Federal Polytechnic, Ado-Ekiti**

The institutional knowledge base is the authoritative repository of verified academic and administrative guidelines powering the FPA Assistant.

---

## 📊 Summary of Knowledge Base Taxonomy (55 Records)

All entries are stored in the PostgreSQL `knowledge_base` table linked to 11 institutional categories:

| ID | Category Name | Record Count | Core Topics Covered |
| :---: | :--- | :---: | :--- |
| **1** | **Admission** | 10 | ND Full-Time cut-offs, Post-UTME screening, Part-Time/Evening entry, HND entry requirements (Lower Credit + 1-yr IT, Pass + 2-yr IT), non-refundable ₦45,000 acceptance fee, overview of 6 academic schools. |
| **2** | **Course Registration** | 6 | Semester online registration steps on the portal, credit unit boundaries (15 min – 24 max), Add/Drop procedure, departmental Course Adviser and HOD approvals. |
| **3** | **School Fees** | 7 | Remita invoice generation, RRR payment verification on portal, resolving unconfirmed bank debits, installment options, Bursary and ICT support emails. |
| **4** | **Examination** | 6 | Mandatory 75% lecture attendance requirement, examination clearance, carryover retakes, NBTE standard grading system (Distinction, Upper Credit, Lower Credit, Pass, Fail). |
| **5** | **Academic Calendar** | 5 | 15-week semester structure, Rector Engr. Dr. Temitope John Alake, Registry, Bursary, Principal Officers, matriculation, and convocation. |
| **6** | **Hostel Services** | 3 | Abuja Hall of Residence, on-campus hall allocations via Student Affairs, safety regulations, prohibited electrical appliances (boiling rings, hot plates). |
| **7** | **SIWES** | 3 | Mandatory 4-month industrial attachment for ND I transitioning to ND II, ITF logbook maintenance, grading and departmental defense. |
| **8** | **Library Services** | 3 | Central Polytechnic Library location, opening hours (Mon–Fri 8AM–6PM, Sat 9AM–2PM), borrower registration, loan durations. |
| **9** | **ICT Support** | 6 | Student portal telephone support (07088391544, 09083892022), support emails (support@lloydant.com, ict@fedpolyado.edu.ng), password reset, ICT Directorate helpdesk. |
| **10** | **Transcript Services** | 2 | Online transcript request procedure via students.fedpolyado.edu.ng, RRR courier fee payment, domestic and international institutional dispatch. |
| **11** | **Graduation Requirements** | 4 | Minimum 2.00 CGPA, institutional final clearance across 6 units (Department, School, Library, Student Affairs, Bursary, Security/Alumni), NYSC mobilization criteria. |

---

## 🏛️ Sourcing & Verification Protocol

Every entry in the knowledge base is verified against official Federal Polytechnic, Ado-Ekiti resources:
- **Official Website**: `https://fedpolyado.edu.ng`
- **Student Portal**: `https://students.fedpolyado.edu.ng`
- **Official Guidelines**: Federal Polytechnic Academic Regulations Handbook, Admissions Directorate notices, Bursary fee circulars, and Student Affairs Division bulletins.

---

## 🛠️ Administrative Management & Maintenance

### 1. In-App Admin Management
Administrators logged in with `joshua@ajala.com` can manage records dynamically:
- Navigate to: `http://localhost:5000/admin`
- **Create Entry**: Click `+ Add Knowledge Entry`, select the category, input the question and verified answer (with optional Markdown), keywords, and source reference.
- **Update Entry**: Click `Edit` on any record row in the table, modify details, and save.
- **Delete Entry**: Click `Delete` to remove obsolete information.

### 2. Database Seeding Files
The repository includes two SQL seeding scripts:
1. `database/schema/knowledge_base_seed.sql`: Initial 24 institutional Q&A entries.
2. `database/schema/knowledge_base_expanded_seed.sql`: 27 comprehensive expanded records covering administrative procedures, leadership, and student services.

```bash
PGPASSWORD=ayoade2004 psql -h localhost -U postgres -d educational_assistant -f database/schema/knowledge_base_seed.sql
PGPASSWORD=ayoade2004 psql -h localhost -U postgres -d educational_assistant -f database/schema/knowledge_base_expanded_seed.sql
```

---

## 🚀 4. Pending Discoveries Queue (`knowledge_candidates`)

To ensure the knowledge repository automatically evolves without manual data entry for new student questions:

1. **Automatic Capture**: When a student asks an inquiry that does not exist in the 55 verified records, Gemini uses Google Search Grounding to fetch the answer and cite source URLs.
2. **Pending Discoveries Card**: The backend stores the discovered Q&A pair in `knowledge_candidates` table with `status = 'pending'`.
3. **One-Click Approval**: In the Admin Portal under the **Pending Discoveries Queue** tab, the administrator can review the discovered answer and click **`Approve to Verified KB`**.
4. **Promotion to KB**: Approving a discovery automatically creates a permanent active entry in `knowledge_base` and marks the candidate status as `approved`. Future queries on that topic hit the verified database directly.
