import boto3
import botocore.config
import json
from datetime import datetime

# Initialize Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1", 
                               config=botocore.config.Config(read_timeout=300, retries={'max_attempts': 3}))

# Function to generate optimized workflow suggestions using Bedrock
def generate_workflow_suggestions(process_data: str) -> str:
    """
    Generate optimized workflow suggestions using AWS Bedrock generative AI.

    Args:
        process_data (str): Historical business process data as input.

    Returns:
        str: Suggested optimized workflows.
    """
    prompt = f"""
    <s>[INST]Human: Analyze the following business process data and suggest optimal workflows for process optimization: \n{process_data}\nAssistant:[/INST]"""

    payload = {
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.5,
        "top_p": 0.9,
        "top_k": 50
    }

    try:
        # Invoke Bedrock model
        response = bedrock.invoke_model(
            body=json.dumps(payload),
            modelId="mistral.mistral-7b-instruct-v0:2",
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response.get("body").read())
        workflow_suggestions = response_body['outputs'][0]['text']
        print(workflow_suggestions)
        return workflow_suggestions

    except Exception as e:
        print(f"Error generating workflow suggestions: {e}")
        return ""

# Function to save the generated workflows to S3
def save_workflow_to_s3(s3_key: str, s3_bucket: str, workflow_suggestions: str):
    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=workflow_suggestions)
        print("Workflow suggestions saved to S3 successfully.")

    except Exception as e:
        print(f"Error saving workflow suggestions to S3: {e}")

# Lambda handler function
def lambda_handler(event, context):
    """
    AWS Lambda handler function to process input data and generate workflow suggestions.
    """
    # Parse event data
    event_body = json.loads(event['body'])
    process_data = event_body['process_data']

    # Generate workflow suggestions
    workflow_suggestions = generate_workflow_suggestions(process_data)

    if workflow_suggestions:
        # Save suggestions to S3
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        s3_key = f"workflow-suggestions/{current_time}.txt"
        s3_bucket = "workflowsuggestionsbucket"  # Replace with your S3 bucket name
        save_workflow_to_s3(s3_key, s3_bucket, workflow_suggestions)

    else:
        print("No workflow suggestions generated.")

    # Return API response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Workflow suggestions generated successfully.',
            'workflow_suggestions': workflow_suggestions
        })
    }
