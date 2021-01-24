import logging.config

import yaml
from vk_api.utils import get_random_id


def msg_construct(vk, msg_recipient, message):
    vk.messages.send(
        peer_id=msg_recipient,
        random_id=get_random_id(),
        message=message
    )


def get_yml_logger(config, name):
    with open(config, "r") as f:
        logging.config.dictConfig(yaml.safe_load(f))
    return logging.getLogger(name)
