FROM python:3.12
WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT python hello_algorithm_test.py $NODE_ID