import boto3

def ensure_dynamodb_table(table_name="SessionTable"):
    dynamodb = boto3.resource("dynamodb")
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "SessionId", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "SessionId", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
        print(f"DynamoDB table {table_name} created.")
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print(f"DynamoDB table {table_name} already exists.")
    return table_name