FROM python:3.7
WORKDIR /QA_Project
COPY . .
RUN pip install Flask 
RUN pip install mysql-connector-python
CMD [ "python3", "app.py" ]
EXPOSE 5000
