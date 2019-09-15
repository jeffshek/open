from config.celery_app import app


@app.task(serializer="json")
def check_services_running():
    print("working!")
