import os
import re
from PyPDF2 import PdfReader
from docx import Document

JOB_KEYWORDS = [
    "python", "flask", "machine learning", "data science", "analytics", "nlp", "aws", "sql", "cloud", "engineering"
]

CONTACT_LABELS = {
    "email", "mail", "phone", "mobile", "contact", "address", "linkedin", "github", "portfolio"
}

SECTION_HEADINGS = {
    "about", "achievements", "certifications", "education", "experience", "languages", "objective",
    "projects", "profile", "skills", "summary", "technical skills", "work experience", "project experience"
}

NON_NAME_LINES = SECTION_HEADINGS | {
    "associate", "bachelor", "bachelors", "master", "masters", "phd", "doctorate", "degree", "diploma",
    "english", "tamil", "hindi", "malayalam", "telugu", "kannada", "french", "german", "spanish"
}

NAME_SUFFIXES = [
    "farith", "kumar", "raj", "ram", "ravi", "babu", "nath", "prasad", "khan", "ali", "ahmed",
    "mohamed", "muhammad", "singh", "sharma", "varma", "gupta", "devi", "priya"
]


def normalize_text(text):
    return re.sub(r"\s+", " ", text.strip().lower())


def read_text_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def read_pdf_file(path):
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)


def read_docx_file(path):
    document = Document(path)
    text = []
    for paragraph in document.paragraphs:
        text.append(paragraph.text)
    return "\n".join(text)


def extract_skills(text):
    raw = normalize_text(text)
    skills = set()
    for keyword in JOB_KEYWORDS:
        if keyword in raw:
            skills.add(keyword.title())
    return sorted(skills)


def extract_experience(text):
    raw = normalize_text(text)
    matches = re.findall(r"(\d+)\+?\s*(?:years|yrs)\b", raw)
    if matches:
        return int(matches[0])
    if re.search(r"\bfresher\b|\bentry[-\s]?level\b|\bintern\b", raw):
        return 0
    return 0


def extract_education(text):
    raw = normalize_text(text)
    education_levels = ["phd", "doctorate", "master", "bachelor", "associate"]
    for level in education_levels:
        if level in raw:
            return level.title()
    return "Professional"


def extract_contact(text):
    email = extract_email(text)
    phone = extract_phone(text)
    return {
        "email": email if email else "Not found",
        "phone": phone if phone else "Not found",
    }


def extract_email(text):
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    if not match:
        return None

    local_part, domain = match.group(0).split("@", 1)
    local_part = clean_email_local_part(local_part)
    return f"{local_part}@{domain}" if local_part else match.group(0)


def clean_email_local_part(local_part):
    cleaned = local_part.strip(".-_+")
    marker_pattern = "|".join(re.escape(marker.replace(" ", "")) for marker in SECTION_HEADINGS | CONTACT_LABELS)
    marker_matches = list(re.finditer(marker_pattern, cleaned, flags=re.IGNORECASE))
    if marker_matches:
        cleaned = cleaned[marker_matches[-1].end():]

    cleaned = re.sub(r"^(?:19|20)\d{2}", "", cleaned)
    cleaned = cleaned.strip(".-_+")
    return cleaned


def extract_phone(text):
    candidates = re.finditer(r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,5}\)?[\s.-]?){2,5}\d{2,5}", text)
    for candidate in candidates:
        value = candidate.group(0).strip()
        digits = re.sub(r"\D", "", value)
        if not 10 <= len(digits) <= 15:
            continue
        if re.fullmatch(r"(?:19|20)\d{2}[\s.-](?:19|20)\d{2}", value):
            continue
        if re.search(r"(?:19|20)\d{2}[\s.-](?:19|20)\d{2}[\s.-](?:19|20)\d{2}", value):
            continue
        return value
    return None


def extract_name(text, filename):
    contact = extract_contact(text)
    if contact["email"] != "Not found":
        local_part = contact["email"].split("@", 1)[0]
        name = infer_name_from_email(local_part)
        if name:
            return name

    name = extract_name_from_top_lines(text)
    if name:
        return name

    filename_name = os.path.splitext(os.path.basename(filename))[0]
    filename_name = re.sub(r"(?i)\b(resume|cv|profile)\b", " ", filename_name)
    filename_name = re.sub(r"[\W_]+", " ", filename_name).strip()
    return filename_name.title() if filename_name else "Not found"


def extract_name_from_top_lines(text):
    for line in text.splitlines()[:10]:
        cleaned = re.sub(r"\s+", " ", line).strip(" -|:")
        if not cleaned:
            continue

        if not is_probable_person_name(cleaned):
            continue
        return cleaned.title()

    return ""


def is_probable_person_name(line):
    lowered = line.lower()
    compact_lowered = re.sub(r"[^a-z]", "", lowered)
    if lowered in NON_NAME_LINES or compact_lowered in {line.replace(" ", "") for line in NON_NAME_LINES}:
        return False
    if is_section_heading_line(line):
        return False
    if is_language_or_proficiency_line(line):
        return False
    if any(label in lowered for label in CONTACT_LABELS):
        return False
    if re.search(r"@|https?://|www\.|\d", line):
        return False

    words = re.findall(r"[A-Za-z]+", line)
    if not 1 <= len(words) <= 4:
        return False
    if len("".join(words)) < 3:
        return False
    return True


def is_language_or_proficiency_line(line):
    lowered = line.lower()
    if re.search(r"\b(native|fluent|proficient|intermediate|beginner|read|write|speak)\b", lowered):
        return True
    compact = re.sub(r"[^a-z]", "", lowered)
    return compact in {line.replace(" ", "") for line in NON_NAME_LINES}


def is_section_heading_line(line):
    lowered = line.lower()
    words = set(re.findall(r"[a-z]+", lowered))
    heading_words = {
        "achievement", "achievements", "certification", "certifications", "education", "experience",
        "language", "languages", "objective", "project", "projects", "profile", "skill", "skills",
        "summary", "technical", "work"
    }
    return bool(words) and words.issubset(heading_words)


def infer_name_from_email(local_part):
    name = re.sub(r"\d+", " ", local_part.lower())
    name = re.sub(r"[\W_]+", " ", name).strip()
    if not name:
        return ""

    parts = name.split()
    if len(parts) > 1:
        return " ".join(part.capitalize() for part in parts)

    compact = parts[0]
    for suffix in NAME_SUFFIXES:
        if compact.endswith(suffix) and compact != suffix and len(compact) - len(suffix) >= 3:
            first = compact[:-len(suffix)]
            return f"{first.capitalize()} {suffix.capitalize()}"
    return compact.capitalize()


def parse_resume(file_path):
    file_type = os.path.splitext(file_path)[1].lower()
    text = ""

    if file_type == ".pdf":
        text = read_pdf_file(file_path)
    elif file_type in {".doc", ".docx"}:
        text = read_docx_file(file_path)
    else:
        text = read_text_file(file_path)

    raw_text = text
    normalized_text = normalize_text(raw_text)
    skills = extract_skills(raw_text)
    experience_years = extract_experience(raw_text)
    education = extract_education(raw_text)
    contact = extract_contact(raw_text)
    contact["name"] = extract_name(raw_text, file_path)
    summary = normalized_text[:1200]

    return {
        "filename": os.path.basename(file_path),
        "content": summary,
        "full_text": normalized_text,
        "skills": skills,
        "experience_years": experience_years,
        "education": education,
        "contact": contact,
        "job_keywords": [keyword.title() for keyword in JOB_KEYWORDS],
    }
