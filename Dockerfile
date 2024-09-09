# Use an official Python 3.12.0 slim image as the base image
FROM python:3.12.0

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1do

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-tk \
        python3-venv \
        python3-pip \
        tini \
        nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/www/html
# RUN useradd -m -s /bin/bash nginx
# USER nginx
COPY ./nginx.conf /etc/nginx/nginx.conf


# Build the app
# COPY --chown=nginx . /var/www/html
# USER root
# Set the working directory in the container
WORKDIR /app
RUN chmod -R 755 /app

# Copy the application code into the container
COPY . /app/

# Create a virtual environment and activate it
RUN python3 -m venv venv
# ENV PATH="venv/bin:$PATH"
RUN /bin/bash -c "source venv/bin/activate && pip install pyserial && deactivate"
# Install Python dependencies
RUN pip install --upgrade pip setuptools-scm
RUN pip install -r requirements.txt

RUN groupadd -r appuser -g 1000 \
    && useradd -r -u 1000 -g appuser -d /app -s /sbin/nologin -c "Docker image user" appuser \
    && chown -R appuser:appuser /app \
    && chown -R appuser:appuser /app/drk/settings.py
    
# RUN useradd -m appuser

# Switch to the appuser
USER appuser

# Expose the port that your Django app runs on
EXPOSE 8000/tcp

# Use tini as the entrypoint
ENTRYPOINT [ "tini", "--"]

# Run the Django development server
# CMD [ "python3", "./manage.py", "runserver", "0.0.0.0:8000" ]
CMD ["gunicorn", "-w", "10", "-b", "0.0.0.0:8000", "--timeout", "0", "drk.wsgi:application"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "drk.wsgi:application"]