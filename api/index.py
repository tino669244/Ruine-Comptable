# api/index.py
#
# Entry point ho an'ny Vercel Serverless Function
# Vercel dia mitady 'app' ao amin'ity file ity

import sys
import os

# Raha ilaina, ampidiro ny lalana amin'ny dossier parent
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app as application  # Maka ilay Flask app avy ao amin'ny main.py

# Vercel dia mitady 'app' anarana
app = application
