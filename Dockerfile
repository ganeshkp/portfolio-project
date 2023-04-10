FROM python:3.8.3-alpine

#Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

# Copy the project
COPY . /usr/src/app

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]   