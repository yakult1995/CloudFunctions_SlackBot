#!/usr/bin/env python
# encoding: utf-8

import json
import requests
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Slack の設定
SLACK_POST_URL = os.environ['SlackPostURL']

def build_message(title, content, color):
    atachements = {
        "title": title,
        "text":content,
        "color":color
    }
    return atachements


def main(request):
    # 引数取得
    request_json = request.get_json()
    # 引数チェック
    if not request_json.keys() >= {"slack_channel", "title", "content", "user_display_name", "color"}:
        return "Params Error"

    # SlackにPOSTする内容をセット
    slack_message = {
        'channel': request_json['slack_channel'],
        "username": request_json['user_display_name'],
        "attachments": [build_message(request_json['title'], request_json['content'], request_json['color'])],
    }

    # SlackにPOST
    try:
        req = requests.post(SLACK_POST_URL, data=json.dumps(slack_message))
        logger.info("Message posted to %s", slack_message['channel'])
    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", e)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 