from vk_api.utils import get_random_id


def msg_construct(vk, msg_recipient, message):
    vk.messages.send(
        peer_id=msg_recipient,
        random_id=get_random_id(),
        message=message
    )


def check_for_owner(response, event):
    for entry in response:
        # If it is the same member as the one who called
        if entry["member_id"] == event.obj.from_id:
            # If the member is admin
            if ("is_admin" in entry and entry["is_admin"]) or ("is_owner" in entry and entry["is_owner"]):
                return True
    return False
