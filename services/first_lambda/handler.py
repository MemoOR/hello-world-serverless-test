import json, os, requests

def hello(event, context):

    enviroment_var = os.environ['MY_VARIABLE']

    try:
        ip = requests.get("http://checkip.amazonaws.com/")
    except requests.RequestException as e:
        print(e)
        raise e
    
    body = {
        "message": "Go Serverless!! deployed correctly with github action",
        "input": enviroment_var
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "location": ip.text.replace("\n", "")
    }

    return response
