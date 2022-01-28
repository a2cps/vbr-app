FROM python:3.9  

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./application /code/application

CMD ["gunicorn", "application.main:app", "--workers", "3", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:5000", "--timeout", "0", "--threads", "2"]
