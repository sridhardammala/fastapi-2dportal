
FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

RUN mkdir /app
ADD . /app/
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# Default port for BentoServer
# EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]



