FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "-OO", "src/run.py"]

EXPOSE 8000
