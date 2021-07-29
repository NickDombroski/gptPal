import os
import json
from slack_sdk import WebClient
from http.server import BaseHTTPRequestHandler, HTTPServer

channel_ID = "C029UL7GFR7"
client = WebClient(token=os.environ['SLACK_API_TOKEN'])

# Sends the given message text in the given channel
# Returns the message value for confirmation
def sendMessageInChannel(channel, message):
    channel_ID = "C029UL7GFR7"
    client = WebClient(token=os.environ['SLACK_API_TOKEN'])
    response = client.chat_postMessage(
        channel=channel,
        text=message
    )
    return response["message"]["text"]

def messageHandler(channel, message):
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
            if body_as_json["event"]["type"] == "message":
                messageHandler(channel_ID, body_as_json["event"]["text"])
        else:
            print("no match")



with HTTPServer(('', 3000), handler) as server:
    server.serve_forever()

