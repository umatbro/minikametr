FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

COPY . /app
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

