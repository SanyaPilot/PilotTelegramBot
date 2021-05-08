FROM python:buster AS build
WORKDIR /usr/src/app

COPY requirements.txt .
RUN python -m venv venv && bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

FROM python:slim
WORKDIR /usr/src/app

RUN apt update && apt upgrade -y

COPY --from=build /usr/src/app/venv ./venv
COPY . .

CMD ["/usr/src/app/venv/bin/python", "./main.py"]
