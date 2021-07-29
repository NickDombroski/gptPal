import os
import json
from slack_sdk import WebClient
from http.server import BaseHTTPRequestHandler, HTTPServer

channel_ID = "C029UL7GFR7"
client = WebClient(token=os.environ['SLACK_API_TOKEN'])

def sendMessageInChannel():
    channel_ID = "C029UL7GFR7"
    client = WebClient(token=os.environ['SLACK_API_TOKEN'])
    response = client.chat_postMessage(
        channel=channel_ID,
        text="I have responded to an event :sunglasses:"
    )
    return response["message"]["text"]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = sendMessageInChannel()
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len)
        body_as_json = json.loads(post_body.decode("utf-8"))
        challenge = (body_as_json["challenge"])
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(bytes(challenge, "utf8"))

with HTTPServer(('', 3000), handler) as server:
    server.serve_forever()

