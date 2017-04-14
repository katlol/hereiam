import settings
import hashlib
import time
from hmac import compare_digest


def create_token(name):
    return hashlib.sha384(f'{name}{settings.hashing_key}'.encode('utf-8')).hexdigest()


def verify_token(name, input_token):
    correct_token = create_token(name)
    return compare_digest(correct_token, input_token)


def timeago(past):
    return int(time.time()) - past
