###########
# BUILDER #
###########

# pull official base image
FROM python:3.11.2-slim as builder

# set work directory
WORKDIR /app

# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# update pip
RUN pip install --upgrade pip
RUN pip install --upgrade wheel

# install python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.11.2-slim

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy project
COPY ./app.py $APP_HOME/app.py
COPY ./config.py $APP_HOME/config.py
COPY ./templates/ $APP_HOME/templates/

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app
