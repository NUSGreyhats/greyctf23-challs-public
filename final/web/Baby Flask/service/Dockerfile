FROM python:3.11

WORKDIR /app

COPY app.py .
COPY requirements.txt .
COPY flag flag/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"] 
