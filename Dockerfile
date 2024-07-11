FROM python:3.11-slim as python-base

# Install necessary system dependencies
RUN apt-get update && \
    apt-get install -y git gcc g++ python3-dev gdal-bin libgdal-dev docker.io

# Allow statements and log messages to appear immediately in the logs
ENV PYTHONUNBUFFERED 1

# Create a non-root user with home directory
RUN useradd -m -u 1000 user

# Add user to the existing 'docker' group
RUN usermod -aG docker user

# Set user and environment variables
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    GDAL_CONFIG=/usr/bin/gdal-config

# Set the working directory in the container
WORKDIR $HOME/app

# Copy the requirements.txt file to the container
COPY requirements.txt $HOME/app/

# Install Python dependencies from requirements.txt
RUN pip install --user -r $HOME/app/requirements.txt

# Copy the application files, including app.py
COPY --chown=user:user . $HOME/app/

# Ensure user has write permission to the app directory
USER root
RUN chmod -R 775 /home/user/.local/lib/python3.11/site-packages/streamlit/static
COPY index.html /home/user/.local/lib/python3.11/site-packages/streamlit/static/index.html
RUN chown -R user:user $HOME/app
USER user

# The application must listen on the port defined by the PORT environment variable.
EXPOSE 8080

# Configure to run TaskWeaver with containerized code execution
ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port", "8080" ]