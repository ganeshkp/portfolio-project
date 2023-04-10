# https://github.com/docker/awesome-compose/blob/master/official-documentation-samples/django/README.md
FROM python:3.8.15

#Set work directory
WORKDIR /code

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the project
COPY . /code/
