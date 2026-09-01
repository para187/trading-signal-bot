import os
from threading import Thread
from flask import Flask

app = Flask('')


@app.route('/')
def home():
  return "Bot ipo hai 24/7 na inaendelea kufanya kazi!"


def run():
  # Render inatoa PORT kiotomatiki kupitia os.environ
  port = int(os.environ.get("PORT", 8080))
  app.run(host='0.0.0.0', port=port)


def keep_alive():
  t = Thread(target=run)
  t.daemon = True
  t.start()
  
