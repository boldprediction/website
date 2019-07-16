from pymemcache.client import base
import json
import hashlib

# Returns a hashed_key when two lists are passed. 
def generate_hash_key(list1,list2):
        combined_key = list1 + list2
        hash224 = hashlib.sha224()
        hash224.update(combined_key.encode('utf-8'))
        return hash224.digest()


# Add's a key value pair into the memcache. If the key already exists,
# it returns false, else returns true when successfully added. 
def add_contrast_into_cache(key,subject):
        #Connect to the client 
        client = base.Client(('localhost',11211))
        result = client.set(key, json.dumps(subject),expire=86400) 
        return result

# Check's if the key value pair exist in the memcache. If yes, then
# it returns the value, else returns a None
def check_contrast_in_cache(key):
        #Connect to the client 
        client = base.Client(('localhost',11211))
        result = client.get(key)
        if result is None:
                return None
        return json.loads(result)
# Check's if the key value pair exist in the memcache. If yes, then
# the key value pair is deleted and returns true, else returns 
# a False if it doesn't exist 
def delete_contrast_in_cache(key):
        #Connect to the client 
        client = base.Client(('localhost',11211))
        result = client.delete(key)
        return result 



        