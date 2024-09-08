from typing import List
from flask import Flask, render_template, request, abort
import os
import base64
import json
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from gmail_functions import get_new_emails, watch_gmail


app = Flask(__name__)
messages: List[str] = []

PUBSUB_VERIFICATION_TOKEN = os.getenv('PUBSUB_VERIFICATION_TOKEN')


@app.route('/')
def index():
    return render_template('index.html', messages=messages)


@app.route('/push-handlers/receive_messages', methods=['POST'])
def receive_messages():
    token = request.args.get('token')
    if token != PUBSUB_VERIFICATION_TOKEN:
        abort(400, description='Invalid token')

    message_data = request.json.get('message', {}).get('data', '')
    decoded_message_data = base64.b64decode(message_data).decode('utf-8')
    new_message_id = json.loads(decoded_message_data)["historyId"]

    messages.append(get_new_emails(new_message_id))
    return '', 200


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def job_listener(event):
    if event.exception:
        logger.error(f'Job failed: {event.job_id}')
        logger.exception(event.exception)
    else:
        logger.info(f'Job completed successfully: {event.job_id}')


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=watch_gmail, trigger="interval",
                      days=1, id='watch_gmail_job')
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()

    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
