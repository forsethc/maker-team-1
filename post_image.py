import json
from slackclient import SlackClient

with open("config.json") as config_file:
    config = json.load(config_file)

sc = SlackClient(config["slack_token"])

def post_image(text, image_url):
    attch = [{
        "text": text,
        "image_url": image_url,
        "color": "danger"
    }]

    sc.api_call(
      "chat.postMessage",
      channel="#team1",
      text="Coffee Update...",
      attachments=attch
    )
