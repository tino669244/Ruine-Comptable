"""
Vercel entrypoint ho an'ny Flask app.
Mitady ilay app ao amin'ny main.py.
"""

import sys
import os

# Raha mila mampiditra modules avy any ivelany (raha misy subfolder)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app as application  # misintona ilay app avy amin'ny main.py

# Vercel mitady "app"
app = application
