FROM python:3.13-alpine

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY /app /app

# Pass version arg
ARG APP_VERSION='docker-dev-build'
RUN echo $APP_VERSION > app_version

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 8080 for Flask
EXPOSE 8080

CMD ["gunicorn","--config", "gunicorn_config.py", "joke_app:app"]
