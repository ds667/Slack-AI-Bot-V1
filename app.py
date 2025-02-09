import os
import json
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import openai

SLACK_BOT_TOKEN = os.getenv("xoxb-2210535565-8426638664740-4NXOX4eixlqTZhwYhReeptpt")
SLACK_SIGNING_SECRET = os.getenv("eebdd636aba2ee7fa4a167e0cc6c6dbc")
OPENAI_API_KEY = os.getenv("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")

slack_client = WebClient(token=SLACK_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})
    if "event" in data:
        event = data["event"]
        if event.get("type") == "message" and "subtype" not in event:
            user_message = event["text"]
            channel_id = event["channel"]
            ai_response = generate_ai_response(user_message)
            send_message(channel_id, ai_response)
    return jsonify({"status": "ok"})

def generate_ai_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                      {"role": "user", "content": user_message}]
        )
        return response["choices"][0]["message"]["content"] + "\n\n_Made by Faizaan Ahmad_"
    except Exception as e:
        return "Error generating response."

def send_message(channel, text):
    try:
        slack_client.chat_postMessage(channel=channel, text=text)
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

if __name__ == "__main__":
    app.run(port=3000)
