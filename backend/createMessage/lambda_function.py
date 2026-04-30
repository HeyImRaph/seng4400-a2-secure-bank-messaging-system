import json
import uuid
import boto3
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("SecureBankMessages")


def lambda_handler(event, context):
    try:
        #   Parse request body from API Gateway
        body = json.loads(event.get("body", "{}"))

        customer_id = body.get("customerId")
        if customer_id:
            customer_id = customer_id.upper()
            
        sender_name = body.get("senderName")
        subject = body.get("subject")
        message_body = body.get("messageBody")

        #   Validate required field
        if not customer_id or not sender_name or not subject or not message_body:
            return response(400, {
                "ERROR": "customerId, senderName, subject, and messageBody are required"
            })

        #   Generate unique IDs for both messages and threads
        message_id = str(uuid.uuid4())
        thread_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()

        item = {
            "messageId": message_id,
            "threadId": thread_id,
            "customerId": customer_id,
            "senderRole": "customer",
            "senderName": sender_name,
            "subject": subject,
            "messageBody": message_body,
            "createdAt": created_at,
            "status": "OPEN"
        }

        #   Store the message in DynamoDB
        table.put_item(Item=item)

        return response(201, {
            "message": "Message created successfully",
            "messageId": message_id,
            "threadId": thread_id,
            "item": item
        })

    except Exception as e:
        return response(500, {
            "ERROR": str(e)
        })


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps(body)
    }