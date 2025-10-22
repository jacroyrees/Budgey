import plaid.api_client
from django.conf import settings
from plaid import Environment
from plaid.api import plaid_api

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def initialise_client():
    client_id = settings.BANKING_CLIENT_ID
    client_secret = settings.BANKING_CLIENT_SECRET
    environment = settings.BANKING_ENVIRONMENT

    if environment == 'production':
        env_type = Environment.Production
    else:  # Default to sandbox for safety
        env_type = Environment.Sandbox
    try:
        configuration = plaid.Configuration(host=env_type, api_key={
            'client_id': client_id,
            'secret': client_secret,
        })
        api_client = plaid.ApiClient(configuration=configuration)
        client = plaid_api.PlaidApi(api_client)
        return client
    except Exception as e:
        print(f"Error initializing Plaid Client: {e}")
        return None

client = initialise_client()