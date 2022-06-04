FROM python:3.8-alpine
WORKDIR /expenselogger
COPY ["src", "requirements.txt", "./"]
# 
# cffi needs libffi-dev libc-dev gcc
# refs: https://stackoverflow.com/questions/57520642/building-a-docker-image-for-a-flask-app-fails-in-pip
# 
RUN apk update \
    && apk add libffi-dev libc-dev gcc \
    && python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT [ "gunicorn" ]
CMD [ "--bind", "0.0.0.0:8000", "main:app" ]
