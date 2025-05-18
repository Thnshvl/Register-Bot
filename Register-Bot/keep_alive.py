from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    print("✅ Hosting at:", f"https://{os.environ['REPL_SLUG']}.{os.environ['REPL_OWNER']}.repl.co")
    t = Thread(target=run)
    t.start()
