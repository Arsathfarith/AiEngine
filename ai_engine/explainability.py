import numpy as np

FEATURE_LABELS = ["Skill count", "Experience years", "Education strength", "Job match ratio"]


def explain_prediction(model, feature_vector, parsed):
    coeffs = model.coef_[0].tolist()
    contributions = []
    for label, value, coef in zip(FEATURE_LABELS, feature_vector, coeffs):
        direction = "positive" if coef >= 0 else "negative"
        contributions.append({
            "feature": label,
            "value": float(value),
            "weight": float(coef),
            "direction": direction,
            "message": f"{label} contributes {'positively' if coef >= 0 else 'negatively'} to the ATS score."
        })

    extra_details = {
        "extracted_skills": parsed["skills"],
        "education": parsed["education"],
        "experience_years": parsed["experience_years"],
    }
    return {"contributions": contributions, "details": extra_details}
