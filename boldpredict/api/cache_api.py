from pymemcache.client import base
import json
from django.conf import settings
from boldpredict.constants import CACHE_EXPIRATION_TIME
# Add's a key value pair into the memcache. If the key already exists,
# it returns false, else returns true when successfully added.

client = base.Client((settings.MAMCACHED_SERVER, settings.MAMCACHED_PORT))

def add_contrast_into_cache(key, contrast_dict):
    # Connect to the client
    try:
        result = client.set(key, json.dumps(contrast_dict), expire=CACHE_EXPIRATION_TIME)
        return result
    except ConnectionRefusedError as cre:
        print("Please start your memcache ", cre)

# Check's if the key value pair exist in the memcache. If yes, then
# it returns the value, else returns a None


def check_contrast_in_cache(key):
    # Connect to the client
    try:
        result = client.get(key)
        if result is None:
            return None
        return json.loads(result)
    except ConnectionRefusedError as cre:
        print("Please start your memcache ", cre)

# Check's if the key value pair exist in the memcache. If yes, then
# the key value pair is deleted and returns true, else returns
# a False if it doesn't exist


def delete_contrast_in_cache(key):
    # Connect to the client
    try:
        result = client.delete(key)
        return result
    except ConnectionRefusedError as cre:
        print("Please start your memcache ", cre)


def update_contrast_in_cache(key, contrast_dict):
    # Connect to the client
    try:
        result = client.set(key, json.dumps(contrast_dict), expire=CACHE_EXPIRATION_TIME)
        return result
    except ConnectionRefusedError as cre:
        print("Please start your memcache ", cre)
