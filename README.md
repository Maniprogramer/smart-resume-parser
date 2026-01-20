# Smart Resume Parser

A **production-style ATS v1 resume parser** built in Python. This project extracts **all first-priority and key second-priority resume details** from unstructured PDF resumes using **rule-based heuristics**, closely mirroring how real-world Applicant Tracking Systems (ATS) work.

The system is designed to be:
- Deterministic where possible (email, phone)
- Heuristic-driven where required (name, experience)
- Idempotent (already-processed resumes are skipped)
- JSON-first (clean structured output)

---

## 🚀 Features

### Tier-1 (First-Priority Resume Data)
- ✅ **Name** (handles single-word and multi-word names)
- ✅ **Email** (regex-based, high accuracy)
- ✅ **Phone number** (robust against OCR noise & dates)
- ✅ **Skills** (keyword-based, configurable skill database)
- ✅ **Experience** (title, company, dates, bullet descriptions)
- ✅ **Education** (degree, institution, date range)
- ✅ **Projects** (project title + bullet descriptions)

### Tier-2 (Secondary but Valuable Data)
- ✅ **Location** (city, state, country with OCR cleanup)
- ✅ **Certifications**

---

## 🧠 Design Philosophy

This project intentionally avoids heavy NLP or ML models.

Real ATS systems:
- Do not "understand" resumes
- Use **regex, heuristics, layout position, and section detection**
- Prefer **precision and usefulness over completeness**

This parser follows the same philosophy:
- Deterministic extraction where patterns are unique
- Probabilistic heuristics where ambiguity exists
- Graceful failure (`null` or empty lists instead of wrong data)

---

## 🏗️ Project Structure

```
smart-resume-parser/
│
├── parser/
│   ├── extractor.py    # PDF → cleaned text extraction
│   ├── fields.py       # Text → structured ATS fields
│   ├── utils.py        # JSON serialization helpers
│
├── resumes/            # Input PDF resumes
├── output/             # Generated JSON output
├── main.py             # Batch processing workflow
├── requirements.txt
└── README.md
```

---

## 🔄 Processing Pipeline

```
PDF Resume
   ↓
Text Extraction (pdfplumber)
   ↓
Text Cleaning
   ↓
Field Extraction (rules + heuristics)
   ↓
Structured JSON Output
```

---

## ▶️ How It Works (Batch Mode)

1. Place PDF resumes inside the `resumes/` directory
2. Run the parser:

```bash
python main.py
```

3. For each resume:
   - If `<resume_name>.json` already exists → **skipped**
   - If not → resume is parsed and saved

4. Output is written to:

```
output/
├── resume1.json
├── resume2.json
```

The process is **idempotent** — re-running the script processes only new resumes.

---

## 📄 Example JSON Output

```json
{
  "name": "Manikanta",
  "email": "manikanta@gmail.com",
  "phone": "8686878787",
  "location": "Kakinada, Andhra Pradesh, India",
  "skills": ["Python", "Java", "AWS", "Docker", "SQL"],
  "education": [
    {
      "degree": "B.S. in Computer Science",
      "institution": "University of Technology India",
      "start_date": "02/2020",
      "end_date": "01/2026"
    }
  ],
  "experience": [
    {
      "title": "Senior Developer",
      "company": "CloudStream Solutions",
      "start_date": "2020",
      "end_date": "Present",
      "description": [
        "Led a team of 5 to migrate legacy infrastructure to AWS",
        "Developed a real-time data processing engine using Python"
      ]
    }
  ],
  "projects": [
    {
      "title": "Resume Parser",
      "description": ["Built an ATS-style resume parser"]
    }
  ],
  "certifications": []
}
```

---

## ⚠️ Known Limitations (Expected)

- Image-only PDFs require OCR (not enabled by default)
- Inline sections without headers may be skipped
- Name extraction is probabilistic, not guaranteed
- Location relies on keyword-based detection

These limitations are **normal for ATS v1 systems**.

---

## 🎯 Why This Project Matters

This project demonstrates:
- Real-world backend data extraction
- Clean separation of concerns
- Idempotent batch processing design
- ATS-style reasoning used in HR tech systems

It is suitable for:
- Python backend roles
- Automation / tooling roles
- Resume parsing systems
- Internship and fresher portfolios

---

## 🔮 Future Improvements

- Confidence scores per extracted field
- OCR fallback for scanned resumes
- Location normalization (city/state/country)
- Skill weighting based on experience
- Resume scoring & ranking

---

## 👤 Author

Built by **Manikan