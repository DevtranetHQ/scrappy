# Read config from environment ("env", "json")
import json
from io import StringIO

TOKEN = "MY TOKEN"
PREFIX = "$"

with open("messages.json") as f:
    message_data = f.read()

MESSAGES = json.load(StringIO(message_data))