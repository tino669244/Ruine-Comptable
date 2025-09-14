from main import app as application

# Vercel handler
def handler(request, *args, **kwargs):
    return application(request, *args, **kwargs)
