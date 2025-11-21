FROM python:3.13

COPY . /GregPilot

WORKDIR /GregPilot

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "4734"]