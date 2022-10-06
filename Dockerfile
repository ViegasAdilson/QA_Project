FROM python:3.10-slim-buster 
WORKDIR /QA_Project
COPY . .
RUN pip install Flask 
RUN pip install mysql-connector-python
CMD [ "python", "app.py" ]
EXPOSE 5000
