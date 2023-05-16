FROM python:3.10-alpine

WORKDIR /code

ENV PYTHONUNBUFFERED=1
ENV POETRY_VER=1.2.2

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip3 install "poetry==$POETRY_VER"
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /code/
RUN poetry install --without dev

COPY . /code/