FROM python:3.10
LABEL maintainer="matinbhdrn"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN  apt-get update && python3 -m pip install --upgrade pip && apt-get install libpq-dev

COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system

RUN apt-get remove -y libpq-dev

COPY . /app/

EXPOSE 8000

ARG DEV=false

# RUN if [ $DEV = "true" ]; \
#         then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
#     fi && \
#     rm -rf /tmp

ENV PATH="/py/bin:$PATH"

