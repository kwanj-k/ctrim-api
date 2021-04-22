# base image  
FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /app  

COPY requirements.txt requirements.txt

COPY ./scripts/ /

# Fix windows docker bug, convert CRLF to LF
RUN sed -i 's/\r$//g' /start.sh && chmod +x /start.sh && sed -i 's/\r$//g' /entrypoint.sh && chmod +x /entrypoint.sh &&\
    sed -i 's/\r$//g' /gunicorn.sh 

# install dependencies  
RUN pip install --upgrade pip  

RUN pip install -r requirements.txt  

COPY . .
# port where the Django app runs  

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]