
from ubuntu:trusty
maintainer Teemu Heikkilä

RUN apt-get update

RUN apt-get install -y build-essential
RUN ln -s /usr/bin/python3.4 /usr/bin/python

RUN apt-get install -y python-dev python-setuptools
RUN easy_install pip

# UWSGI
RUN pip install uwsgi

# Node.js
RUN apt-get -y install curl
RUN curl -sL https://deb.nodesource.com/setup | sudo bash -

RUN apt-get -y install nodejs
RUN npm install -g npm
RUN npm install -g bower

ADD . /app

WORKDIR /app

RUN make clear
RUN apt-get build-dep -y python-psycopg2
RUN apt-get install -y libffi-dev
RUN pip install -r requirements.txt

RUN npm install


# Running tests
RUN make test
RUN rm test.db

EXPOSE 5000

CMD ["uwsgi", "--chdir", "/app/", "uwsgi.ini"]
