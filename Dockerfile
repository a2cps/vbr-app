FROM python:3.9  

# BUILD_VERSION is used to pass commit and date into running app
ARG BUILD_VERSION=
ENV BUILD_VERSION=${BUILD_VERSION}

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./application /code/application

CMD ["gunicorn", "application.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:5000", "--timeout", "0", "--threads", "1"]
