from main import app as application

# Vercel mitady handler
def handler(request, *args, **kwargs):
    return application(request, *args, **kwargs)
