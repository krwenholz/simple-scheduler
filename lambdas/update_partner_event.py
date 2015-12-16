from __future__ import print_function

import json, boto3

print('Loading function')


def lambda_handler(event, context):
    events_table = boto3.resource('dynamodb').Table('simple-scheduler-events')
    for record in event['Records']:
        eventName = record['eventName']
        username = record['dynamodb']['Keys']['username']['S']
        starttime = int(record['dynamodb']['Keys']['starttime']['N'])
        print('Checking event [{}] for [{}, {}]'.format(eventName, username, starttime))
        if eventName == 'INSERT' or eventName == 'MODIFY':
            partner = record['dynamodb']['NewImage']['partner']['S']
            if partner != 'FREE_TIME':
                partner_event = events_table.get_item(Key={'username': partner, 'starttime': starttime})
                if 'Item' not in partner_event:
                    print('Adding partner [{}] meeting to calendar for [{}, {}]'.format(username, partner, starttime))
                    events_table.put_item(Item={'username': partner, 'starttime': starttime, 'partner': username})
        elif eventName == 'REMOVE':
            partner = record['dynamodb']['OldImage']['partner']['S']
            partner_event = events_table.get_item(Key={'username': partner, 'starttime': starttime})
            if 'Item' in partner_event:
                print('Deleting item [{}]'.format(partner_event['Item']))
                events_table.delete_item(Key={'username': partner, 'starttime': starttime})
    return 'Successfully processed {} records.'.format(len(event['Records']))
