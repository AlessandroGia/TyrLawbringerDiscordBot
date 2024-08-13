FROM python:3.11

WORKDIR /app

COPY Pipfile .

RUN pip install pipenv

RUN pipenv install

COPY . .

CMD ["pipenv", "run", "python3", "-u", "main.py"]