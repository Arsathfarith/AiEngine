import numpy as np
from sklearn.linear_model import LogisticRegression

EDUCATION_SCORE = {
    "Phd": 5,
    "Doctorate": 5,
    "Master": 4,
    "Bachelor": 3,
    "Associate": 2,
    "Professional": 1,
}

JOB_MATCH_SKILLS = [
    "Python", "Flask", "Machine Learning", "Data Science", "Analytics", "NLP", "AWS", "SQL", "Cloud", "Engineering"
]


def build_model():
    x = []
    y = []

    sample_profiles = [
        {"skills": 8, "experience": 6, "education": 5, "match": 0.9, "label": 1},
        {"skills": 5, "experience": 3, "education": 4, "match": 0.7, "label": 1},
        {"skills": 2, "experience": 1, "education": 2, "match": 0.2, "label": 0},
        {"skills": 4, "experience": 2, "education": 3, "match": 0.4, "label": 0},
        {"skills": 7, "experience": 5, "education": 4, "match": 0.8, "label": 1},
    ]

    for profile in sample_profiles:
        x.append([profile["skills"], profile["experience"], profile["education"], profile["match"]])
        y.append(profile["label"])

    model = LogisticRegression(solver="liblinear")
    model.fit(np.array(x), np.array(y))
    return model


def build_feature_vector(parsed):
    skill_count = len(parsed["skills"])
    experience_years = parsed["experience_years"]
    education_score = EDUCATION_SCORE.get(parsed["education"], 1)
    match_score = len(set(parsed["skills"]).intersection(JOB_MATCH_SKILLS)) / len(JOB_MATCH_SKILLS)
    return np.array([skill_count, experience_years, education_score, match_score], dtype=float)


def score_resume(parsed, model):
    features = build_feature_vector(parsed)
    probability = float(model.predict_proba([features])[0][1])
    ats_score = round(probability * 100, 1)
    match_score = round(features[3] * 100, 1)
    recommendation = "Strong fit" if probability >= 0.65 else "Consider alternate role" if probability >= 0.35 else "Needs stronger fit"
    feature_metrics = [
        {
            "label": "Skills",
            "value": f"{int(features[0])} found",
            "percent": round(min(features[0] / len(JOB_MATCH_SKILLS), 1) * 100, 1),
        },
        {
            "label": "Experience",
            "value": "Fresher" if int(features[1]) == 0 else f"{int(features[1])} years",
            "percent": round(min(features[1] / 10, 1) * 100, 1),
        },
        {
            "label": "Education",
            "value": parsed["education"],
            "percent": round(min(features[2] / 5, 1) * 100, 1),
        },
        {
            "label": "Job Match",
            "value": f"{match_score}%",
            "percent": match_score,
        },
    ]

    return {
        "feature_vector": features,
        "ats_score": ats_score,
        "match_score": match_score,
        "recommendation": recommendation,
        "feature_metrics": feature_metrics,
    }
