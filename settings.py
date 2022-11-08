import os

MODE = os.environ.get("MODE", "CLI")
TG_BOT_API_TOKEN = os.environ.get("TG_BOT_API_TOKEN", "TG_BOT_API_TOKEN")
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", "HEROKU_APP_NAME")


# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT', 8888))


import json

try:
    with open('local_settings.json') as f:
        data = json.load(f)
        locals().update(data)
except FileNotFoundError:
    pass



# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TG_BOT_API_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'