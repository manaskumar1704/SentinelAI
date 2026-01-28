# 🧭 **CORE PROTOTYPE FLOW**

This prototype follows a **strict, step-by-step flow**.

Nothing happens randomly.

Each stage unlocks the next.

## **High-Level Flow**

1. Landing Page
2. Signup / Login
3. Mandatory Onboarding
4. Dashboard
5. AI Counsellor
6. University Shortlisting
7. University Locking
8. To-Do & Guidance View

---

## 🖥️ **1. LANDING PAGE**

### Purpose

Explain the product in one glance and encourage the user to begin.

### Must Include

- Product name and logo
- Headline:

    > “Plan your study-abroad journey with a guided AI counsellor.”
    >
- Short description (1–2 lines)
- CTA buttons:
  - **Get Started**
  - **Login**

Keep the page minimal and distraction-free.

---

## 🔐 **2. AUTHENTICATION**

### Signup

- Full Name
- Email
- Password
- Google signup (optional)

After signup → onboarding must start immediately.

### Login

- Email + password
- Forgot password (basic functionality is sufficient)

---

## 🧠 **3. USER ONBOARDING (MANDATORY)**

### Purpose

Collect the **minimum required information** to understand the student’s background, goals, and readiness.

Onboarding can be completed in **two modes**:

- Step-by-step manual form
- (Optional bonus) AI-led question flow, where the **AI Counsellor asks questions** (voice-based experience similar to conversational AI)

Both modes must collect the **same underlying data**.

---

### Onboarding Sections (Simplified)

### A. Academic Background

- Current education level
- Degree / major
- Graduation year
- GPA or percentage (optional)

### B. Study Goal

- Intended degree (Bachelor’s / Master’s / MBA / PhD)
- Field of study
- Target intake year
- Preferred countries

### C. Budget

- Budget range per year
- Funding plan:
  - Self-funded
  - Scholarship-dependent
  - Loan-dependent

### D. Exams & Readiness

- IELTS / TOEFL status
- GRE / GMAT status
- SOP status (Not started / Draft / Ready)

---

### Completion Gate

- If onboarding is completed:
  - Profile is marked **Complete**
  - AI Counsellor unlocks
  - Dashboard becomes fully accessible
- If onboarding is incomplete:
  - AI Counsellor remains locked
  - User is prompted to complete onboarding

---

## 📊 **4. DASHBOARD (CONTROL CENTER)**

The dashboard answers **only three questions**:

1. Where am I right now?
2. What should I do next?
3. How strong is my profile?

---

### Dashboard Sections

### A. Profile Summary

- Education
- Target intake
- Countries
- Budget

### B. Profile Strength (AI-Generated)

- Academics: Strong / Average / Weak
- Exams: Not started / In progress / Completed
- SOP: Not started / Draft / Ready

### C. Current Stage Indicator

- Stage 1: Building Profile
- Stage 2: Discovering Universities
- Stage 3: Finalizing Universities
- Stage 4: Preparing Applications

### D. AI To-Do List

- Auto-generated tasks
- Tasks can be marked as completed
- Tasks update automatically when profile or stage changes

---

## 🤖 **5. AI COUNSELLOR (CORE FEATURE)**

### What It Is

The AI Counsellor is a persistent AI agent that understands:

- The user’s profile
- The current stage
- Shortlisted and locked universities

It is available via:

- Chat interface
- (Optional) Voice interface

---

### What the AI Counsellor Can Do

- Explain the user’s profile strengths and gaps
- Recommend universities categorized as:
  - Dream
  - Target
  - Safe
- Clearly explain:
  - Why a university fits
  - Where the risks are
- Shortlist universities directly from the conversation
- Add and update tasks in the to-do list
- Suggest next steps based on the current stage
- Perform key actions within the platform

The AI Counsellor **must take actions**, not just respond with text.

---

## 🎓 **6. UNIVERSITY SHORTLISTING FLOW**

### Step 1: AI Recommendations

Universities are suggested based on:

- User profile
- Budget
- Country preferences
- Competition level

Grouped as:

- Dream
- Target
- Safe

(Dummy or research-based university data is acceptable.)

---

### Step 2: University Evaluation

Each university should display:

- Why it fits the user’s profile
- Key risks
- Cost level (Low / Medium / High)
- Acceptance chance (Low / Medium / High)

---

### Step 3: University Locking (CRITICAL)

- User must lock **at least one university**
- Once locked:
  - Strategy becomes university-specific
  - Application guidance unlocks
- User may unlock later with a clear warning

---

## ✅ **7. APPLICATION GUIDANCE (SIMPLIFIED)**

Unlocked **only after university locking**.

Display:

- Required documents
- High-level timeline
- AI-generated tasks:
  - SOP
  - Exams
  - Forms

No real submissions are required.

---

## 🛠️ **8. PROFILE MANAGEMENT**

- Fully editable profile page
- Any profile edit triggers:
  - Recalculation of university recommendations
  - Task updates
  - Acceptance chance updates

The AI Counsellor must always operate on the **latest profile state**
