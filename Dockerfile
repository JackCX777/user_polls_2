# syntax=docker/dockerfile:1
FROM python:3.9.7
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY ./nanosemantics_web_service ./nanosemantics_web_service
COPY ./config ./config
COPY ./prestart.sh .
RUN chmod +x ./prestart.sh
#RUN ./prestart.sh
#CMD ["python", "nanosemantics_web_service/main.py"]