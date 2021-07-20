import slack
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv
import os
import requests
import feedparser
import time
import re

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

@app.route('/slack2/news', methods = ['POST'])
def news():
    data = request.form
    channel_id = data.get('channel_id')
    arg = data.get('text')
    uid = data.get('user_id')
    
    sources = ['UCLA', 'DailyBruin', 'dailybruin', 'db', 'NYT', 'nyt', 'BBC', 'bbc', 'latimes', 'LATimes']
    
    if (arg == None or arg not in sources):
        client.chat_postEphemeral(user = uid, channel = channel_id, text='Please specify a valid news source. Choose from UCLA, DailyBruin, LATimes, NYT, BBC.')
    else:
        if (arg == 'UCLA'):
            client.chat_postEphemeral(user = uid, channel = channel_id, text='Fetching 5 most recent articles from the UCLA Newsroom...')
            time.sleep(1)
            
            feed = feedparser.parse('http://newsroom.ucla.edu/rss.xml')
            entries = feed['entries']
            parsed = []
            
            for x in range(0, len(entries) - 1, 1):
                if (entries[x].get('author') != None):
                    parsed.append(entries[x]) #should remove any non-articles
            
            blocks = []
            
            for article in range(0, 4, 1):
                blocks.append({
                                "type": "divider"
                            })
                
                blocks.append({
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": '*' + parsed[article]['title'] + '*'
                                },
                                "accessory": {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Read the Story",
                                        "emoji": True
                                    },
                                    "value": "click_me_123",
                                    "url": parsed[article]['link'],
                                    "action_id": "button-action",
                                    'style': 'primary'
                                }
                            })
                
                blocks.append({
                                "type": "context",
                                "elements": [
                                    {
                                        "type": "plain_text",
                                        "text": parsed[article]['published'] + ' | ' + parsed[article]['summary'],
                                        "emoji": True
                                    }
                                ]
                            })
            
            client.chat_postMessage(channel=channel_id, blocks=blocks)
        
        if (arg == 'NYT' or arg == 'nyt'):
            client.chat_postEphemeral(user = uid, channel = channel_id, text='Fetching NYT front page articles...')
            time.sleep(1)
            
            feed = feedparser.parse('https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml')
            entries = feed['entries']
            
            blocks = []
            
            for article in range(0, len(entries)-1, 1):
                blocks.append({
                                "type": "divider"
                            })
                
                blocks.append({
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": '*' + entries[article]['title'] + '*'
                                },
                                "accessory": {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Read the Story",
                                        "emoji": True
                                    },
                                    "value": "click_me_123",
                                    "url": entries[article]['link'],
                                    "action_id": "button-action",
                                    'style': 'primary'
                                }
                            })
                
                blocks.append({
                                "type": "context",
                                "elements": [
                                    {
                                        "type": "plain_text",
                                        "text": entries[article]['published'] + ' | ' + entries[article]['summary'],
                                        "emoji": True
                                    }
                                ]
                            })
            
            client.chat_postMessage(channel=channel_id, blocks=blocks)
        
        if (arg == 'DailyBruin' or arg == 'dailybruin' or arg =='db'):
            client.chat_postEphemeral(user = uid, channel = channel_id, text='Fetching 5 most recent DailyBruin articles...')
            time.sleep(1)
            
            feed = feedparser.parse('https://rss.app/feeds/TQgBGHsMm4rpGUi1.xml')
            entries = feed['entries']
            
            blocks = []
            
            for article in range(0, 4, 1):
                blocks.append({
                                "type": "divider"
                            })
                
                blocks.append({
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": '*' + entries[article]['title'] + '*'
                                },
                                "accessory": {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Read the Story",
                                        "emoji": True
                                    },
                                    "value": "click_me_123",
                                    "url": entries[article]['link'],
                                    "action_id": "button-action",
                                    'style': 'primary'
                                }
                            })
                
                blocks.append({
                                "type": "context",
                                "elements": [
                                    {
                                        "type": "plain_text",
                                        "text": entries[article]['published'] + ' | ' + entries[article]['summary'][0:150].rsplit(' ', 1)[0] + '...',
                                        "emoji": True
                                    }
                                ]
                            })
            
            client.chat_postMessage(channel=channel_id, blocks=blocks)
        
        if (arg == 'BBC' or arg == 'bbc'):
            client.chat_postEphemeral(user = uid, channel = channel_id, text='Fetching 5 most recent BBC - World articles...')
            time.sleep(1)
            
            feed = feedparser.parse('http://feeds.bbci.co.uk/news/world/rss.xml')
            entries = feed['entries']
            
            blocks = []
            
            for article in range(0, 4, 1):
                blocks.append({
                                "type": "divider"
                            })
                
                blocks.append({
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": '*' + entries[article]['title'] + '*'
                                },
                                "accessory": {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Read the Story",
                                        "emoji": True
                                    },
                                    "value": "click_me_123",
                                    "url": entries[article]['link'],
                                    "action_id": "button-action",
                                    'style': 'primary'
                                }
                            })
                
                blocks.append({
                                "type": "context",
                                "elements": [
                                    {
                                        "type": "plain_text",
                                        "text": entries[article]['published'] + ' | ' + entries[article]['summary'],
                                        "emoji": True
                                    }
                                ]
                            })
            
            client.chat_postMessage(channel=channel_id, blocks=blocks)
        
        if (arg == 'latimes' or arg == 'LATimes'):
            client.chat_postEphemeral(user = uid, channel = channel_id, text='Fetching 5 most recent LA Times - California articles...')
            time.sleep(1)
            
            feed = feedparser.parse('https://www.latimes.com/california/rss2.0.xml')
            entries = feed['entries']
            
            blocks = []
            
            for article in range(0, 4, 1):
                blocks.append({
                                "type": "divider"
                            })
                
                blocks.append({
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": '*' + entries[article]['title'] + '*'
                                },
                                "accessory": {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Read the Story",
                                        "emoji": True
                                    },
                                    "value": "click_me_123",
                                    "url": entries[article]['link'],
                                    "action_id": "button-action",
                                    'style': 'primary'
                                }
                            })
                
                blocks.append({
                                "type": "context",
                                "elements": [
                                    {
                                        "type": "plain_text",
                                        "text": entries[article]['published'] + ' | ' + re.search('>(.*)<', entries[article]['summary']).group(1),
                                        "emoji": True
                                    }
                                ]
                            })
            
            client.chat_postMessage(channel=channel_id, blocks=blocks)
                
    return Response(), 200
    
if __name__ == "__main__":
    app.run(debug=True, port=5001)