FROM python:3.11.8 as python-django-celery
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# Create a non-root user and group
RUN groupadd -r celery && useradd -r -g celery celery

# Set permissions for the non-root user on the app directory
RUN chown -R celery:celery /app

# Switch to the non-root user
USER celery
# CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]