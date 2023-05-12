FROM python:3.10

WORKDIR /telegram_bot

COPY requirements.txt .
RUN apt-get update 
RUN apt-get install -y ffmpeg 
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "telegram_bot.py"]