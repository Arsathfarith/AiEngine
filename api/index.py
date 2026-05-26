from vercel_wsgi import handle_request
from app import app


def handler(request, response):
    return handle_request(app, request, response)
