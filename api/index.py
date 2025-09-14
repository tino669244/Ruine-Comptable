import sys
import os

# Ensure root path is added (so main.py, models.py, etc. can be imported)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import create_app

# Create the Flask app
app = create_app()

# ------------------------
# Vercel entrypoint
# ------------------------
def handler(environ, start_response):
    """
    This function is called by Vercel as WSGI entry point.
    It passes the request environ to Flask app.
    """
    return app.wsgi_app(environ, start_response)


# ------------------------
# Local dev test (optional)
# ------------------------
if __name__ == "__main__":
    # Run locally if needed
    app.run(host="0.0.0.0", port=5000, debug=True)
