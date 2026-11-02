"""
Vercel Serverless Function Entry Point for Unbotify.
Exposes the FastAPI application as an ASGI serverless handler.
"""

import sys
import os

# Add project root and src/ to path for Vercel Serverless runtime
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from api import app

# Vercel looks for 'app' in api/index.py

