FROM python:3.8-alpine as build
COPY ["requirements.txt", "./"]
# 
# cffi needs libffi-dev libc-dev gcc
# refs: https://stackoverflow.com/questions/57520642/building-a-docker-image-for-a-flask-app-fails-in-pip
# 
RUN apk update \
    && apk add libffi-dev libc-dev gcc \
    && python -m pip install --upgrade pip \
    && python -m pip wheel --wheel-dir=/wheels -r requirements.txt

FROM python:3.8-alpine
WORKDIR /expenselogger
COPY --from=build /wheels /wheels
COPY ["src", "requirements.txt", "./"]
RUN python -m pip install --upgrade pip \
    && python -m pip install /wheels/*
EXPOSE 8080
ENTRYPOINT [ "gunicorn" ]
CMD [ "--bind", "0.0.0.0:8080", "main:app" ]
