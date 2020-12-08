from vk_api.utils import get_random_id


def msg_construct(vk, msg_recipient, message):
    vk.messages.send(
        peer_id=msg_recipient,
        random_id=get_random_id(),
        message=message
    )
