import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "txt"}
MAX_CONTENT_LENGTH = 8 * 1024 * 1024

SECRET_KEY = os.environ.get("SECRET_KEY", "smart_hire_secret_key")
