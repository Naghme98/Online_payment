# base image
FROM python:3.8
# setup environment variable
ENV StripeHOME=/home/app/webapp

# set work directory
RUN mkdir -p $StripeHOME

# where your code lives
WORKDIR $StripHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip && \
    adduser --disabled-password app -s /bin/sh -h /home/app

# copy whole project to your docker home directory.
COPY . $StripeHOME
# run this command to install all dependencies
RUN pip install -r requirements.txt
# port where the Django app runs

USER app

EXPOSE 8000
# start server
COPY ./command.sh $StripeHOME
RUN chmod -R 777 command.sh
CMD ["/home/app/webapp/command.sh"]
