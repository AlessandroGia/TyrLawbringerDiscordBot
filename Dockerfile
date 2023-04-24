FROM python:3.11

COPY Pipfile .

RUN pip install pipenv

RUN pipenv install

COPY . .

CMD ["pipenv", "run", "python3", "main.py"]