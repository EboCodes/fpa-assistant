-- ====================================================================
-- Comprehensive Knowledge Base Seed for The Federal Polytechnic, Ado-Ekiti
-- Source: Official institutional portal (fedpolyado.edu.ng & students.fedpolyado.edu.ng)
-- ====================================================================

-- 1. ADMISSION
INSERT INTO knowledge_base (category_id, question, answer, keywords, source, status) VALUES
(1, 'What is the acceptance fee for newly admitted students and how do I pay it?', 
'The acceptance fee for newly admitted students into National Diploma (ND) and Higher National Diploma (HND) programmes is non-refundable ₦45,000. 

Payment is strictly made through the official Student Portal (https://students.fedpolyado.edu.ng/) by generating a Remita Retrieval Reference (RRR) invoice under your application profile. Do not pay any fee to private bank accounts or individual agents.', 
'acceptance fee, 45000, new students, admission, remita, payment', 'Admissions Office Official Circular', 'active'),

(1, 'What are the admission requirements for Higher National Diploma (HND) programmes?', 
'Candidates seeking admission into HND programmes must possess:
1. A National Diploma (ND) in the relevant discipline from an NBTE-accredited programme with a minimum of Lower Credit (CGPA of 2.50 or above).
2. A minimum of one (1) year post-ND cognitive industrial work experience (IT). Candidates with a Pass grade at ND level require at least two (2) years of industrial work experience.
3. Five (5) O-Level credit passes in WAEC/NECO/NABTEB at not more than two sittings, including English Language and Mathematics.
4. An official academic transcript forwarded directly to the Registrar of The Federal Polytechnic, Ado-Ekiti before admission can be finalized.', 
'hnd admission, requirements, lower credit, industrial experience, transcript, o level', 'Directorate of Academic Affairs', 'active'),

(1, 'What are the general admission requirements for Full-Time National Diploma (ND)?', 
'For Full-Time ND programmes, applicants must:
1. Score up to or above the national and institutional cut-off mark in the relevant UTME examination.
2. Choose The Federal Polytechnic, Ado-Ekiti as their first-choice institution on the JAMB portal.
3. Possess at least five (5) O-Level credit passes (WAEC/NECO/NABTEB) in relevant subjects, including English Language and Mathematics, obtained in no more than two sittings.
4. Successfully complete the mandatory online Post-UTME screening exercise via the school application portal.', 
'nd admission, requirements, utme, cut off, o level, screening', 'Admissions Directorate', 'active'),

(1, 'Does Federal Polytechnic Ado-Ekiti offer Part-Time or Evening programmes?', 
'Yes, the institution offers National Diploma (ND) and Higher National Diploma (HND) programmes under Part-Time (Evening and Weekend) modes through the Directorate of Continuing Education. 

Part-Time applicants must meet the same standard O-Level requirements (5 credits including English Language and Mathematics). UTME is not compulsory for part-time ND entry, but applicants must register for JAMB Part-Time regularisation.', 
'part time, evening programme, weekend, continuing education, admission', 'Directorate of Continuing Education', 'active'),

(1, 'What academic schools and faculties exist at The Federal Polytechnic, Ado-Ekiti?', 
'The Polytechnic offers academic programmes across major specialized schools:
1. School of Business Studies: Marketing, Public Administration, Business Administration, Procurement & Supply Chain, Liberal Studies.
2. School of Financial Studies: Accountancy, Banking & Finance, Taxation.
3. School of Engineering: Civil Engineering, Electrical/Electronic Engineering, Mechanical Engineering, Agricultural & Bio-Environmental Engineering, Minerals & Petroleum Resources Engineering.
4. School of Environmental Studies: Architectural Technology, Building Technology, Estate Management, Quantity Surveying, Surveying & Geo-Informatics, Urban & Regional Planning, Art & Industrial Design.
5. School of Pure & Applied Sciences: Science Laboratory Technology (SLT), Computer Science, Statistics, Mathematics, Food Technology, Glass & Ceramic Technology, Hospitality Management.
6. School of Agriculture & Agricultural Technology: Agricultural Technology, Fisheries Technology, Horticultural Technology, Animal Health & Production.', 
'schools, faculties, departments, engineering, science, business, environmental, agriculture', 'Academic Planning Unit', 'active');

-- 2. COURSE REGISTRATION
INSERT INTO knowledge_base (category_id, question, answer, keywords, source, status) VALUES
(2, 'What are the credit unit limits for semester course registration?', 
'Students are required to register a minimum of 15 credit units and a maximum of 24 credit units per semester. 

Registering below 15 units or above 24 units requires formal written approval from the Head of Department (HOD) and the Academic Board. Ensure all core and prerequisite courses are prioritized.', 
'credit units, minimum units, maximum units, 15 units, 24 units, course registration', 'Academic Regulations Handbook', 'active'),

(2, 'What is the procedure for adding or dropping a course after registration?', 
'If you need to modify your registered courses:
1. Collect an official Add/Drop Form from your Departmental Secretariat within the first two weeks of semester registration.
2. Consult your Departmental Course Adviser to verify your credit load and course prerequisites.
3. Obtain endorsements from your Course Adviser and Head of Department (HOD).
4. Update your courses on the student portal before the Add/Drop deadline and reprint your revised course registration form.', 
'add drop, change courses, course form, deadline, course adviser', 'Academic Affairs Office', 'active'),

(2, 'Who must sign my semester course registration form?', 
'After completing course registration online, print four (4) copies of the form and obtain signatures in the following order:
1. Departmental Course Adviser
2. Head of Department (HOD)
3. School Officer (Dean’s Office)
Keep your student copy safely, submit one copy to your department, one to the School Officer, and one to the Examination Officer.', 
'course form, signatures, hod, course adviser, school officer, registration', 'Academic Regulations', 'active');

-- 3. SCHOOL FEES & PAYMENTS
INSERT INTO knowledge_base (category_id, question, answer, keywords, source, status) VALUES
(3, 'How do I generate an invoice and pay school fees via Remita?', 
'To pay school fees:
1. Visit the student portal at https://students.fedpolyado.edu.ng/ and log in with your credentials.
2. Navigate to "Fee Payment" and select the current session and semester.
3. Click "Generate Invoice" to obtain your unique 12-digit Remita Retrieval Reference (RRR).
4. Pay online using your debit card or print the invoice and pay at any commercial bank branch in Nigeria.
5. Return to the portal, navigate to "Verify Payment", enter your RRR, and print your official institutional fee receipt.', 
'remita, rrr, invoice, pay school fees, payment receipt, portal', 'Bursary Department', 'active'),

(3, 'What should I do if my payment was deducted but the portal shows unpaid or pending?', 
'If your bank debited you but the portal does not show "Successful":
1. Allow up to 2 hours for inter-bank transaction settlement.
2. Log in to https://students.fedpolyado.edu.ng/, click "Verify Payment", and input your RRR.
3. If the receipt does not generate, send an email to support@lloydant.com and copy ict@fedpolyado.edu.ng.
Include: Your Full Name, Matric/Application Number, RRR Number, Date of Transaction, and Bank Debit Alert or Teller.
You can also visit the ICT Directorate on campus for instant manual clearance.', 
'payment issues, pending payment, rrr verification, support email, bursary, ict', 'ICT Directorate & Bursary', 'active'),

(3, 'Can school fees be paid in installments at Federal Polytechnic, Ado-Ekiti?', 
'The institution approves semester-based payments in line with the approved fee schedule (e.g. paying First Semester fees first, followed by Second Semester fees prior to second semester registration). 

However, full payment for the relevant semester is required before course registration can be finalized and before examination clearance cards are issued.', 
'installments, school fees, semester payment, part payment', 'Bursary Department Circular', 'active');

-- 4. EXAMINATION
INSERT INTO knowledge_base (category_id, question, answer, keywords, source, status) VALUES
(4, 'What is the attendance requirement to be eligible for semester examinations?', 
'Students must attain at least 75% lecture and practical attendance in each registered course to be eligible to sit for semester examinations. 

Course lecturers track attendance throughout the semester. Students falling below 75% without valid medical or official institutional exemption may be barred from writing the examination for that course.', 
'examination eligibility, 75 percent, attendance, exam rules', 'Academic Board Regulations', 'active'),

(4, 'What is the official grading scale and CGPA classification used by the Polytechnic?', 
'The institution operates the National Board for Technical Education (NBTE) standard grading system:
- 75% - 100%: Grade A (4.00) -> Distinction
- 65% - 74%: Grade AB / B (3.00 - 3.49) -> Upper Credit
- 50% - 64%: Grade BC / C (2.50 - 2.99) -> Lower Credit
- 40% - 49%: Grade CD / D (2.00 - 2.49) -> Pass
- Below 40%: Grade F (0.00) -> Fail

A minimum cumulative grade point average (CGPA) of 2.00 is required for the award of an ND or HND certificate.', 
'grading system, cgpa, distinction, upper credit, lower credit, pass, nbte scale', 'Academic Board Policy', 'active'),

(4, 'What happens if a student fails a course or has a carryover?', 
'A student who scores below 40% in a course receives a grade of F and must re-register the course as a carryover in the subsequent academic session during the appropriate semester. 

Carryover courses take precedence over new elective courses, and the total registered credits must not exceed the maximum limit of 24 units per semester.', 
'carryover, fail, retake course, examination, gpa', 'Academic Regulations', 'active');

-- 5. ACADEMIC CALENDAR & LEADERSHIP
INSERT INTO knowledge_base (category_id, question, answer, keywords, source, status) VALUES
(5, 'Who is the current Rector and principal officers of The Federal Polytechnic, Ado-Ekiti?', 
'The Rector of The Federal Polytechnic, Ado-Ekiti is Engr. Dr. Temitope John Alake. 

The management team includes:
- Deputy Rector (Academics)
- Deputy Rector (Administration)
- Registrar
- Bursar
- Polytechnic Librarian
The institution is supervised by the Polytechnic Governing Council and the Federal Ministry of Education.', 
'rector, temitope john alake, principal officers, registrar, bursar, management', 'Institutional Registry', 'active'),

(5, 'How is the academic calendar structured at Federal Polytechnic, Ado-Ekiti?', 
'An academic session consists of two main semesters:
1. First Semester: Typically spans 15 weeks comprising 12 weeks of teaching/lectures, 1 week of revision/matriculation, and 2 weeks of semester examinations.
2. Second Semester: Spans 15 weeks of teaching, student week, revision, and end-of-session examinations, followed by mandatory industrial training/SIWES for qualifying students and long vacation.
Check the official portal (https://fedpolyado.edu.ng) for exact session calendar circulars.', 
'academic calendar, semester duration, weeks, lectures, exams, vacation', 'Academic Planning Directorate', 'active');

-- 6. HOSTEL SERVICES
INSERT INTO knowledge_base (category_id, question, answer, keywords, source, status) VALUES
(6, 'What hostel accommodation options are available on campus and how do I apply?', 
'The Polytechnic provides on-campus residential halls for students, including the Abuja Hall of Residence and designated male and female residential blocks. 

Hostel accommodation is allocated through the Student Affairs Division on a first-come, first-served basis upon full payment of school fees. Bed space application is initiated via the student portal or by obtaining bed space clearance from the Student Affairs Division.', 
'hostel, abuja hall, accommodation, bed space, student affairs', 'Student Affairs Division', 'active'),

(6, 'What items and appliances are prohibited in the student hostels?', 
'To ensure safety and prevent electrical hazards, the following items are strictly prohibited in the campus hostels:
- Electric boiling rings, hot plates, immersion heaters, and electric stoves.
- Gas cylinders and open flame burners.
- Weapons, narcotics, and dangerous implements.
Cooking must strictly be conducted in designated kitchenette areas using authorized equipment.', 
'hostel rules, prohibited items, boiling ring, hot plate, student conduct', 'Student Affairs Division', 'active');

-- 7. SIWES (STUDENTS INDUSTRIAL WORK EXPERIENCE SCHEME)
INSERT INTO knowledge_base (category_id, question, answer, keywords, source, status) VALUES
(7, 'What is the SIWES programme and who is eligible to participate?', 
'The Students Industrial Work Experience Scheme (SIWES) is a mandatory 4-month practical attachment designed to expose students to real-world industrial and engineering practices. 

Eligibility:
- Full-Time ND I students transitioning into ND II in engineering, technology, applied sciences, environmental studies, and agriculture.
- Students must register with the Institutional SIWES Directorate, obtain an official ITF logbook, and submit it with employer evaluations upon resumption.', 
'siwes, industrial training, itf, logbook, nd 1, internship', 'Directorate of SIWES & Industrial Linkages', 'active'),

(7, 'How is the SIWES industrial attachment assessed and graded?', 
'SIWES assessment consists of three components:
1. Institutional supervisor assessment during physical site inspection visits.
2. Employer/Industry-based supervisor evaluation report.
3. Submission of the completed ITF logbook, technical report, and oral departmental presentation/defence.
A passing grade in SIWES is mandatory for National Diploma graduation.', 
'siwes grading, evaluation, logbook assessment, defence, supervisor', 'SIWES Directorate', 'active');

-- 8. LIBRARY SERVICES
INSERT INTO knowledge_base (category_id, question, answer, keywords, source, status) VALUES
(8, 'Where is the Polytechnic Library located and what are the opening hours?', 
'The Central Polytechnic Library is located on the main campus opposite the Administrative Block. 

Opening hours during academic sessions:
- Mondays to Fridays: 8:00 AM – 6:00 PM
- Saturdays: 9:00 AM – 2:00 PM
- Closed on Sundays and public holidays.
Extended hours are maintained during semester examination periods.', 
'library, opening hours, central library, reading, books', 'Polytechnic Library Management', 'active'),

(8, 'How do I register for library cards and borrow books?', 
'To use and borrow resources from the Polytechnic Library:
1. Present your student ID card, admission letter, and official semester fee receipt at the Library Circulation Desk.
2. Complete the Library Registration Form to obtain a Borrower’s Card.
3. Students can borrow up to two (2) books simultaneously for a maximum duration of two (2) weeks, subject to renewal.', 
'borrow books, library card, circulation desk, registration', 'Polytechnic Library Management', 'active');

-- 9. ICT & PORTAL SUPPORT
INSERT INTO knowledge_base (category_id, question, answer, keywords, source, status) VALUES
(9, 'How do I contact official technical support for student portal issues?', 
'For technical support concerning portal login errors, payment validation, or course registration:
- Phone Support: 07088391544, 09083892022 (Available during working hours: 8:00 AM – 4:00 PM)
- Support Email: support@lloydant.com (copy: ict@fedpolyado.edu.ng)
- Physical Location: ICT Directorate, Main Campus, The Federal Polytechnic, Ado-Ekiti.', 
'support phone, ict email, helpdesk, 07088391544, 09083892022, portal problems', 'ICT Directorate', 'active'),

(9, 'How do I reset my student portal password if I forget it?', 
'To reset your password:
1. Go to https://students.fedpolyado.edu.ng/ and click "Forgot Password".
2. Enter your registered Matric Number or Application Number and your registered email address.
3. A password reset link or temporary token will be sent to your email.
4. If you no longer have access to your registered email, visit the ICT Helpdesk on campus with your student ID card for identity verification and manual reset.', 
'forgot password, reset password, student portal, email recovery, ict helpdesk', 'ICT Directorate', 'active');

-- 10. TRANSCRIPT SERVICES
INSERT INTO knowledge_base (category_id, question, answer, keywords, source, status) VALUES
(10, 'How do I apply for an official academic transcript from Federal Polytechnic, Ado-Ekiti?', 
'To apply for an academic transcript:
1. Visit the student portal (https://students.fedpolyado.edu.ng/) and select "Transcript Application".
2. Provide your Matriculation Number, Department, Year of Graduation, and the receiving institution/organization address.
3. Generate an RRR invoice, pay the designated transcript processing and courier fee online via Remita.
4. The Examinations and Records Division will process, verify, and dispatch the transcript directly to the designated institution.', 
'transcript application, request transcript, records, dispatch, remita', 'Examinations & Records Division', 'active');

-- 11. GRADUATION & FINAL CLEARANCE
INSERT INTO knowledge_base (category_id, question, answer, keywords, source, status) VALUES
(11, 'What is the final clearance procedure for graduating students?', 
'Graduating students must complete institutional final clearance across designated units:
1. Departmental Clearance (Head of Department & Project Supervisor)
2. School Officer / Dean of School
3. Polytechnic Central Library (verification of no outstanding books)
4. Student Affairs Division (hostel clearance and union dues)
5. Bursary Division (verification of all session fee receipts)
6. Security Unit and Alumni Association
Once all units endorse your clearance certificate, you are cleared to collect your statement of result or certificate.', 
'final clearance, graduation, bursary clearance, library clearance, statement of result', 'Registry & Academic Affairs', 'active'),

(11, 'What are the requirements for NYSC mobilization of HND graduates?', 
'For HND graduates to be mobilized for the National Youth Service Corps (NYSC):
1. Must have successfully completed the HND programme with all courses passed and obtained academic clearance.
2. Must verify their name on the institutional Senate-approved Mobilization List published by the Student Affairs Division.
3. Must ensure their JAMB Registration Numbers for both ND and HND are regularized and reflected on the NYSC portal.
4. Graduates aged 30 and above at the time of graduation receive an Exemption Certificate in lieu of call-up.', 
'nysc, mobilization, call up letter, hnd graduation, senate list, exemption', 'Student Affairs (NYSC Unit)', 'active');
