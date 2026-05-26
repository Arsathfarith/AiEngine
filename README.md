# SmartHire AI Resume Screening

SmartHire is a Flask-powered resume screening project with AI-driven parsing, skill extraction, ATS scoring, job matching, explainable predictions, and dashboard analytics.

## Features

- Resume upload and parsing
- Skill extraction and keyword matching
- ATS score prediction with explainable AI outputs
- Job matching simulation
- Dashboard analytics and metrics
- Flask templates with static frontend assets
- Local `White.js` frontend helper for layout and interactivity

## Getting Started

1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the environment:

   ```bash
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser.

## Project Structure

- `app.py` - Flask entry point
- `ai_engine/` - resume parsing and AI scoring modules
- `templates/` - Jinja2 templates
- `static/` - CSS and JavaScript files
- `uploads/` - uploaded resumes

## Deployment

This app is ready for deployment on WSGI servers like Gunicorn or uWSGI. Set `FLASK_ENV=production` and serve the app from `app.py`.
