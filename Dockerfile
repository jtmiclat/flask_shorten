FROM python:3.7-slim

LABEL maintainer="Jt Miclat jtmiclat@pez.ai"

ARG PIPENV_ARGS=""

RUN pip install --upgrade pip
RUN pip install pipenv


WORKDIR /flask_shorten

COPY . /flask_shorten
RUN pipenv install --system --deploy  ${PIPENV_ARGS}
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "run:app", "--access-logfile", "-"]
