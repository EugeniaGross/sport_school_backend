FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
# RUN groupadd app-group && useradd -m -G app-group app-user
COPY . .
# RUN chown -R app-user:app-group /app && \
#     chmod 640 /app/.env
# USER app-user
# WORKDIR application/
# CMD gunicorn app:app --workers 4 --forwarded-allow-ips='*' --worker-class main.APIUvicornWorker --bind=0.0.0.0:8000
