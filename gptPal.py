import os
import json
import redis
from slack_sdk import WebClient
from http.server import BaseHTTPRequestHandler, HTTPServer

channel_ID = "C029UL7GFR7"
bot_user_ID = "U029MFZNYBW"
client = WebClient(token=os.environ['SLACK_API_TOKEN'])
r = redis.Redis(host='localhost', port=6379, db=0)
event_ids_key = "events"

# Sends the given message text in the given channel
def sendMessageInChannel(channel, message):
    client = WebClient(token=os.environ['SLACK_API_TOKEN'])
    response = client.chat_postMessage(
        channel=channel,
        text=message
    )

# Handles when a user mentions the bot
def mentionHandler(channel, message, user):
    message = message.replace('<@'+bot_user_ID+'>', 'no u <@'+user+'>')
    sendMessageInChannel(channel, message)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = "If you're seeing this, your get request worked!"
        sendMessageInChannel(channel_ID, message)
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len)
        body_as_json = json.loads(post_body.decode("utf-8"))

        if "challenge" in body_as_json:
            challenge = (body_as_json["challenge"])
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(bytes(challenge, "utf8"))
        elif "event" in body_as_json:
            event = body_as_json["event"]
            print(event["type"])

            set_added_cnt = r.sadd(event_ids_key, body_as_json["event_id"])
            if set_added_cnt == 0:
                print("event already exists")
            elif event["type"] == "app_mention":
                print("handling @mention")
                mentionHandler(channel_ID, event["text"], event["user"])
        else:
            print("no match")



with HTTPServer(('', 3000), handler) as server:
    server.serve_forever()

