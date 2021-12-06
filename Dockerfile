FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
ENV PORT 8080
ENV APP_MODULE application.main:app
ENV LOG_LEVEL debug
ENV WEB_CONCURRENCY 4

COPY ./requirements.txt ./requirements.txt
RUN pip --disable-pip-version-check install -q -U -r ./requirements.txt

COPY env.rc /app/env.rc
COPY ./application /app/application
