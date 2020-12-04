def msg_construct(vk, msg_recipient, random_id, message):
    vk.messages.send(
        peer_id=msg_recipient,
        random_id=random_id,
        message=message
    )
