# Use an official Python base image from the Docker Hub
FROM a5491d878f8c

## Install git
#RUN apt-get -y update
#RUN apt-get -y install git chromium-driver

# Install Xvfb and other dependencies for headless browser testing
#RUN apt-get update \
#    && apt-get install -y wget gnupg2 libgtk-3-0 libdbus-glib-1-2 dbus-x11 xvfb ca-certificates

# Set environment variables
#ENV PIP_NO_CACHE_DIR=yes \
#    PYTHONUNBUFFERED=1 \
#    PYTHONDONTWRITEBYTECODE=1

# Create a non-root user and set permissions
#USER root

# Copy the requirements.txt file and install the requirements
COPY requirements.txt .
#RUN sed -i '/Items below this point will not be included in the Docker Image/,$d' requirements.txt && \
RUN     pip install --no-cache-dir -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com -r requirements.txt

# Copy the application files

# Set the entrypoint
ENTRYPOINT ["python", "-m", "autogptapi"]