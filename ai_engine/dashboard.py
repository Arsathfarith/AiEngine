from collections import Counter

SAMPLE_SUBMISSIONS = [
    {"role": "AI Engineer", "ats": 92, "skills": ["Python", "Machine Learning", "Flask"], "industry": "Technology"},
    {"role": "Data Scientist", "ats": 86, "skills": ["Data Science", "SQL", "Analytics"], "industry": "Finance"},
    {"role": "Product Analyst", "ats": 74, "skills": ["Analytics", "Cloud", "Python"], "industry": "Retail"},
    {"role": "DevOps Specialist", "ats": 68, "skills": ["AWS", "Cloud", "Engineering"], "industry": "Technology"},
]


def compile_dashboard_data():
    avg_score = round(sum(item["ats"] for item in SAMPLE_SUBMISSIONS) / len(SAMPLE_SUBMISSIONS), 1)
    top_skills = Counter(skill for item in SAMPLE_SUBMISSIONS for skill in item["skills"]).most_common(5)
    industry_distribution = Counter(item["industry"] for item in SAMPLE_SUBMISSIONS)
    role_performance = sorted(SAMPLE_SUBMISSIONS, key=lambda item: item["ats"], reverse=True)

    return {
        "average_ats": avg_score,
        "top_skills": top_skills,
        "industry_distribution": industry_distribution,
        "role_performance": role_performance,
        "submissions": SAMPLE_SUBMISSIONS,
    }
