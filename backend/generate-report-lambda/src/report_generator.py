import boto3
import json

import numpy as np


class ReportGenerator:
    def __init__():
        pass

    def run(event):
        # create a DynamoDB client
        ses = boto3.client("ses")
        ses_arn = "arn:aws:ses:us-east-1:412391315699:identity/yl4386@columbia.edu"

        product_id = "/search?q=hello+world"
        message = (
            "Your product report is ready. Please view at this link: https://www.google.com"
            + product_id
        )

        subject = "Your Product Report is Ready"
        body = message
        sender = "yl4386@columbia.edu"
        email = "yl4386@columbia.edu"
        recipients = [email]

        emailContent = {
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": body}},
            "FromEmailAddress": sender,
            "To": [{"EmailAddress": r} for r in recipients],
        }

        sesClient = boto3.client("ses", region_name="us-east-1")

        response = ses.send_email(
            Source=sender,
            Destination={"ToAddresses": recipients},
            Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
        )

        return "success"
