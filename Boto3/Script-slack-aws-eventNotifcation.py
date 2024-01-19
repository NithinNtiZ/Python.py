import requests

def lambda_handler(event, context):
    # Extract variables from the event
    user = event['detail']['userIdentity']['userName']
    event_type = event['detail']['eventName']
    created_on = event['detail']['eventTime']

    # Your Slack webhook URL
    webhook_url = "https://hooks.slack.com/triggers/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"

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
