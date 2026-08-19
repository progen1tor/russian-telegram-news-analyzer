import json 

with open('./config.json', encoding='utf-8') as f: 
    config = json.load(f)
    
API_ID = config['api_id']
API_HASH = config['api_hash']
SESSION_NAME = config['session_name']
TZ = config['timezone']