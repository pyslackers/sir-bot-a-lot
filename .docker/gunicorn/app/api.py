import hug


@hug.get('/')
def say_hi():
    return "Welcome to the default gunicorn demo app"
