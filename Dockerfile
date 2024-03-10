FROM python:3.9-slim

ENV BOT_HOME /bot

WORKDIR $BOT_HOME

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "address_book/run.py"]