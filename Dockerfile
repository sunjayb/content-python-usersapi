# base image
ARG PYTHON_IMAGE
FROM $PYTHON_IMAGE

# working directory
WORKDIR /usr/src/app

# environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

# add/install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy files
COPY . .

# run
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh
