import boto3
import json

import numpy as np


class ReportGenerator:
    def __init__(self):
        pass

    def run(self, frontend_url, product_id, sender_email, receiver_email):
        ses = boto3.client("ses")
        # ses_arn = "arn:aws:ses:us-east-1:412391315699:identity/yl4386@columbia.edu"

        analysis_link = f"{frontend_url}/analyses/{product_id}"
        message = f"Your product report is ready. Please view at this link: {analysis_link}"

        subject = "Your Product Report is Ready"
        body = message
        recipients = [receiver_email]

        """
        emailContent = {
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": body}},
            "FromEmailAddress": sender_email,
            "To": [{"EmailAddress": r} for r in recipients],
        }
        """
        print(analysis_link)
        """
        sesClient = boto3.client("ses", region_name="us-east-1")

        response = ses.send_email(
            Source=sender,
            Destination={"ToAddresses": recipients},
            Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
        )
        """
        return {"statusCode": 200, "body": "Success!"}
