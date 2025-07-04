
FROM python:3.9-slim-buster



WORKDIR /app


COPY requirements.txt .


RUN python -m myworld myworld && \
    myworld/bin/pip install --no-cache-dir --upgrade pip && \
    myworld/bin/pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 8000


CMD ["myworld/bin/waitress-serve", "--listen=0.0.0.0:8000", "app:app"]