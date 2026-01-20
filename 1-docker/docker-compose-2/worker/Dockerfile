FROM python:3.10-alpine

WORKDIR /code

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "worker.py"]