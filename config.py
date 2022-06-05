"""CONFIG"""
import json
from io import StringIO
from collections import namedtuple

print("\n~Importing CONFIG~\n")

# Read config from environment ("env", "json")
with open("texts.json") as f:
    text_data = f.read()

# Read config from environment ("env", "json")
with open("secrets.json") as f:
    secret_data = f.read()


# To allow access like `config.MESSAGE.WELCOME_MESSAGE`
text_data = json.loads(text_data)
TEXT_FIELDS = namedtuple("TEXT_FIELDS", text_data.keys())
TEXT = TEXT_FIELDS(**text_data)

# To allow access like `config.MESSAGE.WELCOME_MESSAGE`
secret_data = json.loads(secret_data)
SECRET_FIELDS = namedtuple("SECRETS_FIELDS", secret_data.keys())
SECRETS = SECRET_FIELDS(**secret_data)

DISCORD_TOKEN = SECRETS.DISCORD_TOKEN
PREFIX = "$"

PERSIST_POSTS_INTERVAL = 1  # seconds
PERSIST_POST_ENDPOINT = "http://httpbin.org"
