FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 80

CMD ["flask", "--app", "app", "run", "--host", "0.0.0.0", "--port", "80"]
