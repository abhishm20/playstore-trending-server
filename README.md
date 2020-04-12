## Notes

- Used Mysql-8.0
- Used Celery with Redis for background tasks
- Used flower to monitor background tasks
- Configured production and local environment. For real world scenario, one can also add development and staging environment.
- Used Gunicorn with Supervisor to run the server
- Used nginx for API server
- For better performance we can increase celery worker count by putting celery-worker server in Auto Scaling.
- I have put all the configuration in project/bin folder to setup on server


## To run

1. Install dependencies:

    `pip install -r requirements.txt`

2. To load customers in DB

    `python manage.py runscript setup_server`
    
3. Run celery

    `celery -A project.celery_config worker -l info -Q default_queue --concurrency=4 -O fair`

4. Run flower to monitor celery tasks

    `flower -A project.celery_config --port=5555 --url-prefix=flower`

5. Run server

    `python manage.py runserver`
    
## Demo

`open 3.85.8.66 for listing`

`open this 3.85.8.66/flower`