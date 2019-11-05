import json
import logging
import os
import time
import uuid
from contextlib import contextmanager
from datetime import datetime

import connexion
from azure.eventhub import EventHubClient, EventData, EventHubError

server_id = str(uuid.uuid4())
producer = None
server_name = ""

if 'SERVER_NAME' in os.environ:  # Change this to log to azure locally
    server_name = os.environ['SERVER_NAME']
    EVENT_HUB_CONNECTION_STRING = os.environ['EVENT_HUB_CONNECTION_STRING']
    EVENT_HUB_PATH = os.environ['EVENT_HUB_PATH']

    client = EventHubClient.from_connection_string(EVENT_HUB_CONNECTION_STRING, event_hub_path=EVENT_HUB_PATH)
    producer = client.create_producer(partition_id="0")


def info(**kwargs):
    _log_to_event_hub(level="info", **kwargs)
    logging.info(f'msg:{kwargs.get("message", "None")} {kwargs.get("elapsed", "")}')


def warning(**kwargs):
    _log_to_event_hub(level="warning", **kwargs)
    logging.warning(f'msg:{kwargs.get("message", "None")} {kwargs.get("elapsed", "")}')


def error(**kwargs):
    _log_to_event_hub(level="error", **kwargs)
    logging.error(f'msg:{kwargs.get("message", "None")} {kwargs.get("elapsed", "")}')


def get_md5_username():
    try:
        return connexion.context['token_info']['md5_username']
    except KeyError:
        return "development"
    except AttributeError:
        return "system"


def setup_logging():
    logging.basicConfig(
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        level=logging.INFO,
        handlers=[
            logging.StreamHandler()
        ])


def _log_to_event_hub(**kwargs):
    try:
        if producer is not None:
            md5_username = get_md5_username()
            producer.send(EventData(json.dumps({
                "md5_username": md5_username,
                "server_name": server_name,
                "server_id": server_id,
                "timestamp": str(datetime.now()),
                **kwargs
            })))
    except EventHubError as e:
        logging.error(f"Could not log to event hub: {e}")


@contextmanager
def timed(**kwargs):
    start_time = time.time()
    yield start_time
    info(elapsed=time.time() - start_time, **kwargs)


@contextmanager
def _timed_without_event_hub(**kwargs):
    start_time = time.time()
    yield start_time
    logging.info(f'{kwargs["message"]} {str(time.time() - start_time)}')

