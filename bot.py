import praw
import base64
import requests
import json
import time
import logging
import conversion
import subprocess

logging.basicConfig(level=logging.INFO)

def do_mention(mention, reddit_object, api_key):
    reddit_object.inbox.mark_read([mention])
    parent = mention.parent()
    text = parent.body
    logging.info(f"{mention.author} wrote:\n\n{mention.body}\n\nUnder:{text}")
    
    try:
        font_size = int(mention.body.split(" ")[1])
    except Exception:
        font_size = 50

    post_url = parent.submission.url
    r = requests.get(post_url)
    with open("image.jpg", "wb") as f:
        f.write(r.content)

    conversion.image_edit("image.jpg", text, "out.jpg", font_size)

    url = upload_to_imgbb("out.jpg", api_key)

    mention.reply(f"Here is your processed image:\n{url}\n\nIt will be available for 10 minutes.\n\nThis bot adds a comment to the bottom of the posted image.")

def upload_to_imgbb(file, api_key):
    with open(file, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": api_key,
            "image": base64.b64encode(file.read()),
        }
        res = requests.post(url, payload)
    data = json.loads(res.content)
    return str(data['data']['url'])

# Enter your Reddit credentials here
reddit = praw.Reddit(client_id = 'xxxxxxxxxxxxxx',
                            client_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx',
                            username = 'your_username',
                            password = 'your_password',
                            user_agent = 'fdfdghzjtjfg') # this can be anything you want

# This is your ImgBB API Key
imgbb_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

while 1:

    for mention in reddit.inbox.unread(limit=None):
        try:
            do_mention(mention, reddit, imgbb_key)
        except AttributeError:
            pass

