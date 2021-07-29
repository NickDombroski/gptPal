import os
from slack_sdk import WebClient

channel_ID = "C029UL7GFR7"
client = WebClient(token=os.environ['SLACK_API_TOKEN'])
response = client.chat_postMessage(
    channel=channel_ID,
    text="Hello world!")
assert response["ok"]
assert response["message"]["text"] == "Hello world!"