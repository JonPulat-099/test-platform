FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/

RUN apt-get -y update && apt-get install -y build-essential  python3-dev  python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info wkhtmltopdf
RUN pip install -r requirements.txt
RUN apt remove python3-openssl
RUN find /usr -name '*.pyc' -delete
RUN pip install --upgrade --force-reinstall setuptools
COPY . /code/
# RUN python manage.py migrate


RUN adduser --disabled-password --gecos '' myuser