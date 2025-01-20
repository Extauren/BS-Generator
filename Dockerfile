FROM python:3.13.1-slim-bullseye

WORKDIR /app

RUN apt-get update

RUN apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libjpeg-dev libopenjp2-7-dev libffi-dev

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY bs_generator.py .
COPY data.py .
COPY templates ./templates

CMD ["python", "bs_generator.py", "-h"]