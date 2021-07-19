'''
Created on Jul 19, 2021

@author: Private
'''
'''
Created on Jul 13, 2021

@author: Private
'''

import slack
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv
import os
import requests, json

load_dotenv()

signing = os.environ.get("signing")
slack_token = os.environ.get("slack")

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(signing, '/slack/events', app)
client = slack.WebClient(token = slack_token)

bot_id = client.api_call("auth.test")['user_id']

client.conversations_open(users='U01EJSDGX50')
client.chat_postMessage(channel='D028X1MUDED', text='Bot is now online!')


@app.route('/slack2/joke', methods=['POST'])
def joke():
    data = request.form
    channel_id = data.get('channel_id')
    
    #get joke from https://github.com/15Dkatz/official_joke_api
    url = "https://official-joke-api.appspot.com/random_joke"
    r = requests.get(url)
    data = r.json()
    setup = data['setup']
    punchline = data['punchline']
    
    client.chat_postMessage(channel = channel_id, blocks=[
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": setup
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*" + punchline + "*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Jokes from <https://github.com/15Dkatz/official_joke_api>"
                }
            ]
        }])
    
    return Response(), 200
    
if __name__ == "__main__":
    app.run(debug=True)