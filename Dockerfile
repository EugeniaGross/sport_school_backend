FROM python:3.12
WORKDIR app/
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN groupadd app-group && useradd -G app-group app-user
RUN chown -R app-user:app-group /app
USER app-user
# WORKDIR application/
# CMD gunicorn app:app --workers 4 --forwarded-allow-ips='*' --worker-class main.APIUvicornWorker --bind=0.0.0.0:8000
