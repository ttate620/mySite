FROM python:3.7

ENV WEBAPP_DIR=/mysite

RUN mkdir $WEBAPP_DIR
WORKDIR $WEBAPP_DIR
ADD static_cdn .
ADD requirements.txt $WEBAPP_DIR/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt