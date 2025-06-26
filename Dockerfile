FROM python:3.12

RUN mkdir aviation-carbon

COPY . aviation-carbon

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools wheel
RUN pip3 install -r aviation-carbon/requirements.txt