import json
import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("SecureBankMessages")


def lambda_handler(event, context):
    try:
        path_params = event.get("pathParameters") or {}
        customer_id = path_params.get("customerId")

        if customer_id:
            customer_id = customer_id.upper()
            result = table.scan(
                FilterExpression=Attr("customerId").eq(customer_id)
            )
        else:
            result = table.scan()

        messages = result.get("Items", [])
        messages.sort(key=lambda x: x.get("createdAt", ""))

        return response(200, {
            "customerId": customer_id if customer_id else "ALL",
            "messages": messages
        })

    except Exception as e:
        return response(500, {
            "error": str(e)
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