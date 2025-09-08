from langchain_aws import BedrockEmbeddings
import boto3
import sys
from botocore.exceptions import BotoCoreError, ClientError

def get_bedrock_embedding(region_name="us-east-1", model_id="amazon.titan-embed-text-v2:0"):
    """
    Initialize AWS Bedrock client and return a BedrockEmbeddings object.

    """
    try:
        # Initialize AWS Bedrock client
        client = boto3.client("bedrock-runtime", region_name=region_name)
    except (BotoCoreError, ClientError) as e:
        print(f"Failed to initialize AWS Bedrock client: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        # Initialize Bedrock Embeddings
        embedding = BedrockEmbeddings(model_id=model_id, client=client)
    except Exception as e:
        print(f"Failed to initialize Bedrock Embeddings model: {e}", file=sys.stderr)
        sys.exit(1)

    return embedding
