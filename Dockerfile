FROM python:3.9-slim

WORKDIR /app

RUN pip install poetry && poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-dev

COPY . /app
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

