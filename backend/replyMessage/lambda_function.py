import json
import uuid
import boto3
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("SecureBankMessages")


def lambda_handler(event, context):
    try:
        #   Grabbing thread ID from request path
        path_params = event.get("pathParameters") or {}
        thread_id = path_params.get("threadId")

        #   Parsing request body for staff reply details
        body = json.loads(event.get("body", "{}"))

        staff_name = body.get("staffName")
        message_body = body.get("messageBody")

        #   Validating required fields for reply
        if not thread_id or not staff_name or not message_body:
            return response(400, {
                "ERROR": "threadId, staffName, and messageBody are required"
            })

        #   Finding existing messages in the same thread
        thread_result = table.scan(
            FilterExpression=Attr("threadId").eq(thread_id)
        )

        thread_messages = thread_result.get("Items", [])

        if len(thread_messages) == 0:
            return response(404, {
                "ERROR": "Thread not found"
            })

        original_message = thread_messages[0]

        message_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()

        #   Create new reply linked to original thread
        item = {
            "messageId": message_id,
            "threadId": thread_id,
            "customerId": original_message["customerId"],
            "senderRole": "staff",
            "senderName": staff_name,
            "subject": original_message["subject"],
            "messageBody": message_body,
            "createdAt": created_at,
            "status": "REPLIED"
        }

        #   Saving reply message to DynamoDB
        table.put_item(Item=item)

        return response(201, {
            "message": "Reply saved successfully",
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