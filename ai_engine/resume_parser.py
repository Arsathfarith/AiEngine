import os
import re
from PyPDF2 import PdfReader
from docx import Document

JOB_KEYWORDS = [
    "python", "flask", "machine learning", "data science", "analytics", "nlp", "aws", "sql", "cloud", "engineering"
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
    matches = re.findall(r"(\d+)\+?\s+years", raw)
    if matches:
        return int(matches[0])
    return 1


def extract_education(text):
    raw = normalize_text(text)
    education_levels = ["phd", "doctorate", "master", "bachelor", "associate"]
    for level in education_levels:
        if level in raw:
            return level.title()
    return "Professional"


def extract_contact(text):
    email = re.search(r"[\w\.-]+@[\w\.-]+", text)
    phone = re.search(r"\+?\d[\d\s\-]{7,}\d", text)
    return {
        "email": email.group(0) if email else "Not found",
        "phone": phone.group(0) if phone else "Not found",
    }


def parse_resume(file_path):
    file_type = os.path.splitext(file_path)[1].lower()
    text = ""

    if file_type == ".pdf":
        text = read_pdf_file(file_path)
    elif file_type in {".doc", ".docx"}:
        text = read_docx_file(file_path)
    else:
        text = read_text_file(file_path)

    text = normalize_text(text)
    skills = extract_skills(text)
    experience_years = extract_experience(text)
    education = extract_education(text)
    contact = extract_contact(text)
    summary = text[:1200]

    return {
        "filename": os.path.basename(file_path),
        "content": summary,
        "full_text": text,
        "skills": skills,
        "experience_years": experience_years,
        "education": education,
        "contact": contact,
        "job_keywords": [keyword.title() for keyword in JOB_KEYWORDS],
    }
