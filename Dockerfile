FROM python:3.10
LABEL maintainer="matinbhdrn"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN  apt-get update && python3 -m pip install --upgrade pip && apt-get install libpq-dev
    # && apt-get install jpeg-dev && apt-get install zlib && apt-get install zlib-dev

COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system

RUN apt-get remove -y libpq-dev
#   && apt-get remove -y zlib && apt-get remove -y zlib-dev

COPY . /app/

EXPOSE 8000

ARG DEV=false

# RUN if [ $DEV = "true" ]; \
#         then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
#     fi && \
#     rm -rf /tmp
RUN mkdir -p /vol/web/media && mkdir -p /vol/web/static && chmod -R 755 /vol
ENV PATH="/py/bin:$PATH"

