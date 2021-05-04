FROM python:slim
WORKDIR /usr/src/app

RUN apt update && apt upgrade -y

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main.py"]
