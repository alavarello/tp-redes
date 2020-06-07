# Use the official image as a parent image.
FROM python:latest

# Set the working directory.
WORKDIR /usr/src/app

# Run the command inside your image filesystem.

RUN pip install psycopg2 Flask-SQLAlchemy Flask-Migrate
RUN pip install flask
RUN pip install flask_restful

# Copy the file from your host to your current location.
COPY api/ .

# Run the specified command within the container.
CMD [ "python", "api.py" ]

EXPOSE 8888
