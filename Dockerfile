FROM python:3.11

WORKDIR /app

COPY Pipfile .

RUN pip install pipenv

RUN pipenv install

COPY . .

RUN apt-get update && apt-get install -y ffmpeg

CMD ["pipenv", "run", "python3", "-u", "main.py"]