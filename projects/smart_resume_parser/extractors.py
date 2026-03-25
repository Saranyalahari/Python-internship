import re

# -------------------------
# SECTION HELPERS
# -------------------------

SECTION_HEADERS = [
    "objective",
    "skills",
    "professional experience",
    "employment history",
    "experience",
    "education",
    "certifications",
    "courses",
    "references",
    "languages",
    "hobbies",
    "details",
    "links",
    "profile",
]

STOPWORDS_SKILLS = {
    "skills", "objective", "references", "certifications", "education",
    "experience", "professional experience", "employment history",
    "details", "links", "profile", "languages", "hobbies",
    "brooklyn ny", "erlanger ky", "tel", "phone", "email"
}

DEGREE_WORDS = [
    "bachelor", "master", "b.tech", "btech", "m.tech", "mtech",
    "b.e", "be", "b.sc", "bsc", "m.sc", "msc", "phd",
    "associate", "associates", "degree", "diploma", "university",
    "college", "school"
]

JOB_TITLE_WORDS = [
    "manager", "engineer", "developer", "analyst", "assistant",
    "associate", "executive", "officer", "consultant", "intern",
    "specialist", "technician", "supervisor", "lead", "designer",
    "administrator", "coordinator"
]


def normalize_text(text):
    text = text.replace("\r", "\n")
    text = re.sub(r'\n+', '\n', text)
    return text


def clean_line(line):
    line = line.strip()
    line = re.sub(r'^[•\-\*\u2022]+\s*', '', line)
    line = re.sub(r'\s+', ' ', line)
    return line.strip(" ,:-")


def get_section(text, section_name):
    """
    Extract only the content under a given section until the next known section header.
    """
    text_lower = text.lower()
    start_pattern = re.compile(rf'(^|\n)\s*{re.escape(section_name)}\s*(\n|$)', re.IGNORECASE)
    start_match = start_pattern.search(text_lower)

    if not start_match:
        return ""

    start_idx = start_match.end()

    next_positions = []
    for header in SECTION_HEADERS:
        if header.lower() == section_name.lower():
            continue
        pattern = re.compile(rf'(^|\n)\s*{re.escape(header)}\s*(\n|$)', re.IGNORECASE)
        m = pattern.search(text_lower, start_idx)
        if m:
            next_positions.append(m.start())

    end_idx = min(next_positions) if next_positions else len(text)
    return text[start_idx:end_idx].strip()


# -------------------------
# EMAIL
# -------------------------

def extract_email(text):
    emails = re.findall(
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
        text
    )
    return emails[0] if emails else None


# -------------------------
# SKILLS
# -------------------------

def is_valid_skill_line(line):
    low = line.lower()

    if not line or len(line) < 2:
        return False
    if any(ch.isdigit() for ch in line):
        return False
    if len(line.split()) > 6:
        return False
    if low in STOPWORDS_SKILLS:
        return False
    if re.search(r'@|www|http|tel|phone', low):
        return False
    if re.search(r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b', low):
        return False
    if re.search(r'\b(ky|ny|fl|ca|tx)\b', low):
        return False
    if any(word in low for word in ["college", "university", "reference", "certification", "manager,"]):
        return False

    return True


def extract_skills(text):
    section = get_section(text, "skills")
    if not section:
        return []

    skills = []
    for raw_line in section.split("\n"):
        line = clean_line(raw_line)
        if is_valid_skill_line(line):
            skills.append(line)

    # remove duplicates while preserving order
    unique_skills = []
    seen = set()
    for skill in skills:
        key = skill.lower()
        if key not in seen:
            seen.add(key)
            unique_skills.append(skill)

    return unique_skills


# -------------------------
# EDUCATION
# -------------------------

def extract_education(text):
    section = get_section(text, "education")
    if not section:
        return []

    education = []
    lines = [clean_line(line) for line in section.split("\n") if clean_line(line)]

    for line in lines:
        low = line.lower()

        if re.search(r'\b(' + '|'.join(re.escape(word) for word in DEGREE_WORDS) + r')\b', low):
            education.append(line)

    unique_education = []
    seen = set()
    for item in education:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            unique_education.append(item)

    return unique_education


# -------------------------
# EXPERIENCE
# -------------------------

def looks_like_job_title(line):
    low = line.lower()

    if len(line.split()) > 12:
        return False
    if re.search(r'^[•\-\*]', line):
        return False
    if re.search(r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\d{4})\b', low):
        return False
    if any(word in low for word in ["responsible", "performed", "utilize", "maintain", "loaded", "operated"]):
        return False

    return any(word in low for word in JOB_TITLE_WORDS)


def extract_experience(text):
    section = get_section(text, "professional experience")
    if not section:
        section = get_section(text, "employment history")
    if not section:
        section = get_section(text, "experience")
    if not section:
        return []

    jobs = []
    lines = [clean_line(line) for line in section.split("\n") if clean_line(line)]

    for line in lines:
        if looks_like_job_title(line):
            jobs.append(line)

    unique_jobs = []
    seen = set()
    for job in jobs:
        key = job.lower()
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    return unique_jobs