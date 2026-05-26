import os
import tempfile
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from ai_engine.resume_parser import parse_resume
from ai_engine.scoring import score_resume, build_model
from ai_engine.dashboard import compile_dashboard_data
from ai_engine.explainability import explain_prediction
import config

app = Flask(__name__)
app.config.from_object(config)
if os.path.isdir(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

MODEL = build_model()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/parse", methods=["POST"])
def parse_upload():
    if "resume" not in request.files:
        flash("No file part in request.")
        return redirect(request.url)

    file = request.files["resume"]
    if file.filename == "":
        flash("No file selected.")
        return redirect(request.url)

    if not allowed_file(file.filename):
        flash("Unsupported file type. Use PDF, DOC, DOCX, or TXT.")
        return redirect(request.url)

    filename = secure_filename(file.filename)
    with tempfile.TemporaryDirectory() as temp_dir:
        save_path = os.path.join(temp_dir, filename)
        file.save(save_path)
        parsed = parse_resume(save_path)

    result = score_resume(parsed, MODEL)
    explanation = explain_prediction(MODEL, result["feature_vector"], parsed)

    context = {
        "parsed": parsed,
        "ats_score": result["ats_score"],
        "match_score": result["match_score"],
        "recommendation": result["recommendation"],
        "explanation": explanation,
        "filename": filename,
    }

    return render_template("results.html", **context)


@app.route("/dashboard")
def dashboard():
    analytics = compile_dashboard_data()
    return render_template("dashboard.html", analytics=analytics)


@app.route("/analytics")
def analytics():
    analytics = compile_dashboard_data()
    return render_template("analytics.html", analytics=analytics)


if __name__ == "__main__":
    app.run(debug=True)
