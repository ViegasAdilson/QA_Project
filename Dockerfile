FROM python:3.7
ADD . /qa_project
WORKDIR /qa_project
COPY . .
RUN pip install Flask
RUN pip install mysql-connector-python
CMD [ "python3", "./app.py" ]
EXPOSE 5000
