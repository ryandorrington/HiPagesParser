from typing import List
from flask import Flask, render_template
import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from gmail_functions import watch_gmail


app = Flask(__name__)
messages: List[str] = []


@app.route('/')
def index():
    return render_template('index.html', messages=messages)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def job_listener(event):
    if event.exception:
        logger.error(f'Job failed: {event.job_id}')
        logger.exception(event.exception)
    else:
        logger.info(f'Job completed successfully: {event.job_id}')


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=watch_gmail, trigger="interval", m=1, id='watch_gmail_job')
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()

    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)