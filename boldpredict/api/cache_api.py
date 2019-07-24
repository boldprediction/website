from pymemcache.client import base
import json
from django.conf import settings
import logging
# Add's a key value pair into the memcache. If the key already exists,
# it returns false, else returns true when successfully added.

client = base.Client((settings.MAMCACHED_SERVER, settings.MAMCACHED_PORT))
logger = logging.getLogger("django")


def set_contrast_in_cache(key1,key2,contrast_dict):
    # Connect to the client
    try:
        value = json.dumps(contrast_dict)
        result = client.set(key1, value, expire=settings.CACHE_EXPIRATION_TIME)
        logger.info('set cache with key' + key1 )
        result = client.set(key2, value, expire=settings.CACHE_EXPIRATION_TIME)
        logger.info('set cache with key' + key2 )
        return result
    except ConnectionRefusedError as cre:
        logger.error('Memcache connection error, cache did not start' )

# Check's if the key value pair exist in the memcache. If yes, then
# it returns the value, else returns a None


def check_contrast_in_cache(key):
    # Connect to the client
    try:
        logger.info('try to get record with key' + key + ' from Memcache' )
        result = client.get(key)
        if result is None:
            return None
        return json.loads(result)
    except ConnectionRefusedError as cre:
        logger.error('Memcache connection error, cache did not start' )

# Check's if the key value pair exist in the memcache. If yes, then
# the key value pair is deleted and returns true, else returns
# a False if it doesn't exist


def delete_contrast_in_cache(id_key,hash_key):
    # Connect to the client
    try:
        result = client.delete(id_key)
        result = client.delete(hash_key)
        return result
    except ConnectionRefusedError as cre:
        logger.error('Memcache connection error, cache did not start' )
