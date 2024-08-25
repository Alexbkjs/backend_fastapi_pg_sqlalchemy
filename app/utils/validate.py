import hmac
import hashlib
import urllib.parse
import json
from fastapi import HTTPException
import time

def validate_init_data(init_data_raw: str, bot_token: str) -> dict:
    """
    Validate the initial data received from the client.

    - **init_data_raw**: The raw data to verify.
    - **bot_token**: The bot token used for HMAC validation.

    Returns the parsed parameters if validation succeeds, raises an HTTPException otherwise.
    """
    # Parse initDataRaw into a dictionary
    params = dict(x.split('=', 1) for x in init_data_raw.split('&'))

    # Decode the 'user' field from URL encoding
    params['user'] = urllib.parse.unquote(params.get('user', ''))

    # Extract and decode user data
    user_data_str = params.get('user', '')
    try:
        user_data_str = urllib.parse.unquote(user_data_str)  # URL-decode the user data string
        user_data = json.loads(user_data_str) if user_data_str else {}  # Parse JSON data
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid user data format")

    # Create the data_check_string for HMAC validation
    data_check_string = '\n'.join(f"{key}={value}" for key, value in sorted(params.items()) if key != "hash")

    # Create the secret key with HMAC
    secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()

    # Generate the HMAC hash for validation
    calculated_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    # Compare the calculated hash with the provided hash
    if calculated_hash != params.get("hash", ""):
        raise HTTPException(status_code=400, detail="Invalid hash")
    
    # Uncomment if needed to validate auth_date for outdated data
    current_time = int(time.time())
    if current_time - int(params["auth_date"]) > 86400:  # Check if it's older than 24 hours
        raise HTTPException(status_code=400, detail="Outdated data")
    
    # Everyting is good otherwise!

    return params
