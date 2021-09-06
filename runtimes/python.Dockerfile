FROM python:3.9
WORKDIR /app
RUN pip install numpy pandas

ENTRYPOINT ["python3"]