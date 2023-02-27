FROM python:3.10-slim-buster
# Copy only requirements to cache them in docker layer:
WORKDIR /usr
COPY . .
RUN pip install --upgrade pip
RUN pip install pika && pip install aio-pika

# Set the python path:
ENV PYTHONPATH="$PYTHONPATH:${PWD}"


CMD ["python", "-u", "run_worker.py"]
