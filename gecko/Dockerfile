FROM python:3.9-slim-buster


WORKDIR .

COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

COPY . .

EXPOSE 4004

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4004"]