import secrets


def _generate_random_token(_len=25):
    return secrets.token_urlsafe(_len)


def _generate_room_random_id(_len=30):
    return secrets.token_urlsafe(_len)


def _generate_random_token_25(_len=25):
    return secrets.token_urlsafe(_len)
