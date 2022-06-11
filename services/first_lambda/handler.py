import os
import json
import boto3
import random
import string

def genMessageDeduplicationId(chars = string.ascii_uppercase + string.digits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))

def lambda_handler(event, context):
    sqs = boto3.client('sqs')
    
    queue1_name = os.environ['QUEUE1_NAME']
    queue2_name = os.environ['QUEUE2_NAME']
    
    groupId = os.environ['MessageGroupId']
    
    queue1 = sqs.get_queue_url(QueueName=queue1_name)
    queue2 = sqs.get_queue_url(QueueName=queue2_name)
    
    json_dict = {
        "op": "pago",
    }
    
    json_dict = json.dumps(json_dict)
    
    response = sqs.send_message(
        QueueUrl=queue1['QueueUrl'],
        MessageBody = json_dict,
        
        # Necesarios por ser lista fifo
        MessageGroupId = groupId, 
        MessageDeduplicationId = genMessageDeduplicationId()
    )
    
    print(response)
    print("Looking this Id:")
    print(response['MessageId'])
    
    # genero el name del key de los Message attributes
    id = 'id' + response['MessageId']
    print("waiting for:")
    print(id)
    
    results = sqs.receive_message(
        QueueUrl=queue2['QueueUrl'],
        AttributeNames=[
            'All'
        ],
        MaxNumberOfMessages=10,
        MessageAttributeNames=['All'],  
        VisibilityTimeout=5, # importante para poder borrar el mensaje con código
        WaitTimeSeconds=10 # tiempo que va a esperar la función a que haya algún mensaje
    )
    
    if len(results) > 0:

        for i in range(len(results['Messages'])):
            if id in results['Messages'][i]['MessageAttributes']:
                print("found")
                
                message = results['Messages'][i]
                receipt_handle = message['ReceiptHandle'] # se usa para borrar el mensaje
                
                # Aqui se obtiene el mensaje donde viene el id de la base de datos,
                # guardar aqui el dato en alguna variable para que se borre de 
                # forma eficiente el mensaje
                
                print("The id is:")
                print(message['MessageAttributes'][id]['StringValue'])
                print("the random is:")
                print(message['MessageAttributes']['randomNumber']['StringValue'])

                # Importante borrar el mensaje para que se vean los siguientes
                # al hacer otro request
                sqs.delete_message(
                    QueueUrl=queue2['QueueUrl'],
                    ReceiptHandle=receipt_handle
                )
                break
    else:
        print("no data")
    
    return {
        'statusCode': 200,
        'body': json.dumps('SQS request made')
    }