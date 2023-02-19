FROM python:3.9
WORKDIR /app
COPY ./ .
RUN pip install -r requirements.txt
EXPOSE 8001
CMD ["gunicorn", "-b", "0.0.0.0:8001", "--workers", "2", "app:app"]

