FROM python:3.10-slim-buster 
ADD . /Agenda
WORKDIR /Agenda 
COPY . .
RUN pip install Flask 
Run pip install mysql-connector-python
CMD [ "python", "./app.py" ]
