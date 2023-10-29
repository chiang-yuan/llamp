FROM python:3.11-slim

EXPOSE 8000

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y build-essential git

COPY . .

RUN pip install -e .

CMD ["uvicorn", "llamp.main:app", "--host", "0.0.0.0", "--port", "8000"]