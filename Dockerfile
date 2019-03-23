FROM python:3.7-slim
MAINTAINER Jt Miclat


# Start Installing the Basic Dependencies
RUN pip install --upgrade pip
RUN pip install poetry


WORKDIR /flask_shorten

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install -n --no-dev
COPY . /flask_shorten
CMD ["poetry", "run", "gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "wsgi:app", "--access-logfile", "-"]
