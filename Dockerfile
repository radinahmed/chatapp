FROM  python:3.7.4-alpine3.10

WORKDIR /root

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install PyMySQL
#RUN pip install mysqlclient


EXPOSE 8080

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
CMD /wait && python app.py