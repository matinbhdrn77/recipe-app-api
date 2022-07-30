FROM python:3.9-alpine3.13
LABEL maintainer="matinbhdrn"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN  apk add --update --no-cache postgresql-client && \
     apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev

COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system

RUN apk del .tmp-build-deps

COPY . /app/

EXPOSE 8000

ARG DEV=false

# RUN if [ $DEV = "true" ]; \
#         then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
#     fi && \
#     rm -rf /tmp
RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user

