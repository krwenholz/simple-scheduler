############################################################
# Dockerfile to build a Python WSGI application container 
# fronted by nginx
############################################################

# Set the base image to Ubuntu
FROM ubuntu 

# File Author / Maintainer
MAINTAINER Kyle R Wenholz

# Add the application resources URL
RUN apt-get update

# Install basic applications
RUN apt-get install -y git vim wget dialog net-tools
RUN apt-get install -y python3-pip nginx supervisor

# Add the app
ADD ./app /app

# Get pip to download and install requirements:
RUN pip3 install -r /app/requirements.txt

# Copy configuration files from the current directory
ADD config/nginx.conf /etc/nginx/nginx.conf
RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
RUN ln -s ./config/supervisor.conf /etc/supervisor/conf.d/

# Expose nginx port
EXPOSE 80

# Use supervisord to start nginx and flask
CMD ["supervisord", "-n"]
