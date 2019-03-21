FROM python:3.7-slim
MAINTAINER Jt Miclat


# Start Installing the Basic Dependencies
RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config settings.virtualenvs.create false

WORKDIR /flask_shorten

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install -n --no-dev
COPY . /flask_shorten



ENTRYPOINT ["python", "run.py"]

