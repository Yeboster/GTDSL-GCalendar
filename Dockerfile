FROM python:3.8-slim-buster

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pipenv requirements
RUN python -m pip install pipenv gunicorn
COPY Pipfile* ./
RUN python -m pipenv install --system --deploy

WORKDIR /app
ADD . /app

RUN useradd appuser && chown -R appuser /app 
RUN mkdir /home/appuser && chown -R appuser /home/appuser
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "gcalendar.api:api"]
