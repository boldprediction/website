from pymemcache.client import base
import json
from django.conf import settings
import logging
# Add's a key value pair into the memcache. If the key already exists,
# it returns false, else returns true when successfully added.

logger = logging.getLogger("django")


def set_contrast_in_cache(id_key,hash_key,contrast_dict):
    # Connect to the client
    client = base.Client((settings.MAMCACHED_SERVER, settings.MAMCACHED_PORT))
    try:
        value = json.dumps(contrast_dict)
        result = client.set(id_key, value, expire=settings.CACHE_EXPIRATION_TIME)
        logger.info('set cache with key ' + id_key )
        result = client.set(hash_key, value, expire=settings.CACHE_EXPIRATION_TIME)
        logger.info('set cache with key ' + hash_key )
        return result
    except ConnectionRefusedError as cre:
        logger.error('Memcache connection error, cache did not start' )

# Check's if the key value pair exist in the memcache. If yes, then
# it returns the value, else returns a None

def check_contrast_in_cache(key):
    client = base.Client((settings.MAMCACHED_SERVER, settings.MAMCACHED_PORT))
    # Connect to the client
    try:
        logger.info('try to get record with key ' + str(key) + ' from Memcache' )
        result = client.get(str(key))
        if result is None:
            return None
        return json.loads(result)
    except ConnectionRefusedError as cre:
        logger.error('Memcache connection error, cache did not start' )

# Check's if the key value pair exist in the memcache. If yes, then
# the key value pair is deleted and returns true, else returns
# a False if it doesn't exist


def delete_contrast_in_cache(id_key,hash_key):
    client = base.Client((settings.MAMCACHED_SERVER, settings.MAMCACHED_PORT))
    # Connect to the client
    try:
        result = client.delete(str(id_key))
        logger.info('Delete record with key ' + str(id_key) + ' from Memcache' )
        result = client.delete(str(hash_key))
        logger.info('Delete record with key ' + str(hash_key) + ' from Memcache' )
        return result
    except ConnectionRefusedError as cre:
        logger.error('Memcache connection error, cache did not start' )
