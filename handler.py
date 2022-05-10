import json
import os
import requests

def hello(event, context):
    enviroment_var = os.environ['MY_VARIABLE']
    
    body = {
        "message": "Go Serverless!! deployed correctly with github action",
        "input": enviroment_var
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
