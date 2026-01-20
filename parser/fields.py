import re
from typing import Dict, Optional


EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)

PHONE_REGEX = re.compile(
    r"(\+?\d{1,3}[\s-]?)?\(?\d{3,4}\)?[\s-]?\d{3}[\s-]?\d{4}"
)

DATE_RANGE_REGEX = re.compile(
    r"(\d{2}/\d{4})\s*[–-]\s*(\d{2}/\d{4})"
)

EXPERIENCE_DATE_REGEX = re.compile(
    r"(\d{4})\s*[–-]\s*(Present|\d{4})",
    re.IGNORECASE
)

LOCATION_KEYWORDS = [
    "india", "usa", "united states", "uk", "canada",
    "australia", "andhra pradesh", "telangana",
    "tamil nadu", "karnataka", "maharashtra"
]

SECTION_HEADERS = [
    "skills", "education", "experience", "profile",
    "projects", "certifications", "achievements"
]

SKILLS_DB = {
    "python": "Python",
    "java": "Java",
    "c++": "C++",
    "c": "C",
    "javascript": "JavaScript",
    "html": "HTML",
    "css": "CSS",
    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "mongodb": "MongoDB",
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "data science": "Data Science",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scikit-learn": "Scikit-learn",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "opencv": "OpenCV",
    "nlp": "NLP",
    "git": "Git",
    "github": "GitHub",
    "linux": "Linux",
    "docker": "Docker",
    "aws": "AWS"
}

DEGREE_KEYWORDS = [
    "b.s", "b.sc", "b.tech", "b.e", "bachelor",
    "m.s", "m.sc", "m.tech", "m.e", "master",
    "phd", "doctorate", "diploma"
]

SECTION_HEADERS = [
    "skills", "education", "experience", "profile",
    "projects", "certifications", "achievements"
]


def extract_skills(text: str) -> list:
    """
    Extract skills using keyword matching.
    Returns list of detected skills.
    """
    text_lower = text.lower()
    found_skills = set()

    for keyword, skill_name in SKILLS_DB.items():
        if keyword in text_lower:
            found_skills.add(skill_name)

    return sorted(found_skills)


def extract_email(text: str) -> Optional[str]:
    matches = EMAIL_REGEX.findall(text)
    return matches[0] if matches else None


def extract_phone(text: str) -> Optional[str]:
    # Normalize unicode dashes
    text = text.replace("–", "-").replace("—", "-")

    candidates = re.findall(r"\+?\d[\d\s\-()]{8,}\d", text)

    for candidate in candidates:
        digits = re.sub(r"\D", "", candidate)

        # Typical phone number length
        if 10 <= len(digits) <= 13:
            return candidate.strip()

    return None



def extract_name(text: str) -> Optional[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    blacklist = [
        "resume", "curriculum", "vitae", "email", "phone",
        "mobile", "@", "linkedin", "github", "skills",
        "engineer", "developer", "automation", "profile",
        "education", "university", "college"
    ]

    skill_keywords = set(SKILLS_DB.keys())

    # ---------- PASS 1: MULTI-WORD NAMES ----------
    for line in lines[:6]:
        lower = line.lower()

        if any(word in lower for word in blacklist):
            continue
        if any(skill in lower for skill in skill_keywords):
            continue

        words = line.split()

        if 2 <= len(words) <= 4:
            clean = re.sub(r"[^a-zA-Z ]", "", line)
            if clean.replace(" ", "").isalpha():
                return clean.strip()

    # ---------- PASS 2: SINGLE-WORD NAME (TOP ONLY) ----------
    first_line = lines[0]
    lower_first = first_line.lower()

    if (
        first_line.isalpha()
        and first_line[0].isupper()
        and len(first_line) >= 3
        and lower_first not in skill_keywords
        and not any(word in lower_first for word in blacklist)
    ):
        return first_line

    return None

def extract_education(text: str) -> list:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    education = []

    in_education_section = False

    for i, line in enumerate(lines):
        lower = line.lower()

        # Detect EDUCATION section
        if lower == "education":
            in_education_section = True
            continue

        if in_education_section:
            # Stop if another section starts
            if lower in ["skills", "experience", "profile", "projects"]:
                break

            # Detect degree line
            if any(keyword in lower for keyword in DEGREE_KEYWORDS):
                degree = line
                institution = None
                start_date = None
                end_date = None

                # Look for dates in same line
                date_match = DATE_RANGE_REGEX.search(line)
                if date_match:
                    start_date, end_date = date_match.groups()
                    degree = DATE_RANGE_REGEX.sub("", degree).strip()

                # Institution usually next line
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if not any(k in next_line.lower() for k in DEGREE_KEYWORDS):
                        institution = next_line

                education.append({
                    "degree": degree,
                    "institution": institution,
                    "start_date": start_date,
                    "end_date": end_date
                })

    return education

def extract_projects(text: str) -> list:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    projects = []

    in_projects_section = False
    current_project = None

    for line in lines:
        lower = line.lower()

        # Detect PROJECTS section
        if lower == "projects":
            in_projects_section = True
            continue

        if in_projects_section:
            # Stop when another section starts
            if lower in SECTION_HEADERS and lower != "projects":
                break

            # Bullet point → project description
            if line.startswith(("•", "-", "*")) and current_project:
                desc = line.lstrip("•-* ").strip()
                current_project["description"].append(desc)
                continue

            # New project title (non-bullet, short line)
            if not line.startswith(("•", "-", "*")):
                # Save previous project
                if current_project:
                    projects.append(current_project)

                current_project = {
                    "title": line,
                    "description": []
                }

    # Append last project
    if current_project:
        projects.append(current_project)

    return projects

def extract_experience(text: str) -> list:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    experience = []

    in_experience_section = False
    current_role = None

    for line in lines:
        lower = line.lower()

        # Detect EXPERIENCE / PROFILE section
        if lower in ["experience", "work experience", "profile"]:
            in_experience_section = True
            continue

        # Stop when another section starts
        if in_experience_section and lower in [
            "education", "skills", "projects", "certifications"
        ]:
            break

        if not in_experience_section:
            continue

        # Bullet point → description
        if line.startswith(("•", "-", "*")) and current_role:
            desc = line.lstrip("•-* ").strip()
            current_role["description"].append(desc)
            continue

        # Role | Company | Date line
        if "|" in line:
            date_match = EXPERIENCE_DATE_REGEX.search(line)

            if date_match:
                start_date, end_date = date_match.groups()

                parts = [p.strip() for p in line.split("|")]

                title = parts[0] if len(parts) > 0 else None
                company = parts[1] if len(parts) > 1 else None

                # Save previous role
                if current_role:
                    experience.append(current_role)

                current_role = {
                    "title": title,
                    "company": company,
                    "start_date": start_date,
                    "end_date": end_date,
                    "description": []
                }

    # Append last role
    if current_role:
        experience.append(current_role)

    return experience

def extract_location(text: str) -> Optional[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in lines[:10]:
        lower = line.lower()

        if any(keyword in lower for keyword in LOCATION_KEYWORDS):
            # Remove email
            line = re.sub(
                r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
                "",
                line
            )

            # Remove phone numbers
            line = re.sub(
                r"\+?\d[\d\s\-()]{8,}\d",
                "",
                line
            )

            # Remove common OCR garbage characters
            line = re.sub(r"[|()]", " ", line)

            # Remove isolated single letters like 'n'
            line = re.sub(r"\b[a-zA-Z]\b", " ", line)

            # Normalize spaces
            line = re.sub(r"\s{2,}", " ", line)

            # Clean commas
            line = re.sub(r"\s*,\s*", ", ", line)

            location = line.strip(" ,")

            # Final sanity check
            if "," in location and len(location) >= 5:
                return location

    return None

def extract_certifications(text: str) -> list:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    certifications = []

    in_cert_section = False

    for line in lines:
        lower = line.lower()

        # Detect CERTIFICATIONS section
        if lower == "certifications":
            in_cert_section = True
            continue

        # Stop when another section starts
        if in_cert_section and lower in SECTION_HEADERS:
            break

        if in_cert_section:
            # Remove bullets if present
            clean = line.lstrip("•-* ").strip()

            # Basic sanity check
            if len(clean) >= 5:
                certifications.append(clean)

    return certifications


def extract_basic_fields(text: str) -> Dict[str, Optional[str]]:
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "location": extract_location(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "projects": extract_projects(text),
        "experience": extract_experience(text),
        "certifications": extract_certifications(text)
    }




