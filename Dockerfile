#using alpine as lightversion of Linux
FROM python:3.9-alpine3.13
LABEL mainteiner="stojchevskimartin"

#recommended when running django in docker container
ENV PYTHONUNBUFFERED=1


#copies the requierments.txt into new dir /tmp/
COPY ./requirements.txt /tmp/requirements.txt
#copies the requierments.dev.txt into new dir /tmp/
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
#copies the app dir into new /app dir
COPY ./app /app
#setting the working dir
WORKDIR /app
#exposing the port from the container to the machine
EXPOSE 8000

ARG DEV=false
#runs on the image that is built
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

#adding the system path for the image
ENV PATH="/py/bin:$PATH"

USER django-user
