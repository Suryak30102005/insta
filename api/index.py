# api/index.py
from app import app
from vercel_wsgi import run_wsgi

def handler(event, context):
    return run_wsgi(app, event, context)
