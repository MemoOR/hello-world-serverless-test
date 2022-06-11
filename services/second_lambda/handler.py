import os
import json
import boto3
import random
import string

def genMessageDeduplicationId(chars = string.ascii_uppercase + string.digits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))

def lambda_handler(event, context):
    # TODO implement
    print(event['Records'][0]['messageId'])
    sqs = boto3.client('sqs')
    
    queue_name = os.environ['QUEUE_NAME']
    queue = sqs.get_queue_url(QueueName=queue_name)
    
    groupId = os.environ['MessageGroupId']
    
    # obtengo el id del mensaje recibido y genero el nombre del key para los
    # message attributes
    id = 'id' + event['Records'][0]['messageId']
    
    print("sending to:")
    print(id)

    
    # JSON para mandar los message attributes
    messageAttribs = {
            id: {
            'DataType': 'String',
            'StringValue': event['Records'][0]['messageId']
        }, 
        # aqui iria el id de la base de datos
            'randomNumber': {
            'DataType': 'Number',
            'StringValue': str(random.randint(0,9))
        }
    }

    print(messageAttribs)
    
    response = sqs.send_message(
        QueueUrl=queue['QueueUrl'],
        MessageBody = (
            'Here is the response body'
        ),
        MessageAttributes = messageAttribs,
        # Necesarios por ser lista fifo
        MessageGroupId = groupId, 
        MessageDeduplicationId = genMessageDeduplicationId()
    )
    
    print(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Successful request made')
    }