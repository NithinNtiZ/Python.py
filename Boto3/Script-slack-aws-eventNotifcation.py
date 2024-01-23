import requests

def lambda_handler(event, context):
    # Extract variables from the event
    if event['detail']['userIdentity']['type'] == "IAMUser":
        user = event['detail']['userIdentity']['userName']
    else:
        user = event['detail']['userIdentity']['principalId']



    event_type = event['detail']['eventName']
    created_on = event['detail']['eventTime']
    # Your Slack webhook URL
    webhook_url = ""

    # Your message data (you can customize this according to your needs)
    message = {
        "text": f"user: {user}\tEventType: {event_type}\tCreateOn: {created_on}"
    }

    # Send the POST request to the Slack webhook URL
    response = requests.post(webhook_url, json=message)

    # Check the response status
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

    # Return a response (optional)
    return {
        'statusCode': response.status_code,
        'body': response.text
    }
