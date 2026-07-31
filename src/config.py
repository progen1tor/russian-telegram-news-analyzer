import json 
from constants import CONFIG_PATH

with open(CONFIG_PATH, encoding='utf-8') as f: 
    config = json.load(f)
    
API_ID = config['api_id']
API_HASH = config['api_hash']
SESSION_NAME = config['session_name']
TZ = config['timezone']