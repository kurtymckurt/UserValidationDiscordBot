FROM python:3

ADD .env /
ADD bot.py /
ADD GlobalBotConfig.py /

RUN pip install discord.py
RUN pip install python-dotenv
RUN pip install tinydb

CMD [ "python", "./bot.py", "db.json" ]